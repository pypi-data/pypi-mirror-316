import logging
import os
import signal
from typing import Any, AsyncGenerator

import aiohttp
import anyio
import mcp.server.stdio
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.types import ImageContent, TextContent, Tool

from . import __version__
from .endpoint import EndpointManager, PortRange

logger = logging.getLogger(__name__)


class MCPServer:
    """MCP server for JetBrains IDE proxy."""

    def __init__(self) -> None:
        """Initialize MCP server."""
        self.server = Server('jetbrains/proxy')
        self.endpoint_manager = EndpointManager(
            port_range=PortRange(start=63342, end=63352), tools_changed_callback=self._on_tools_changed
        )
        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Set up MCP request handlers."""

        @self.server.list_tools()  # type: ignore
        async def handle_list_tools() -> AsyncGenerator[Tool, None]:
            """Handle list tools request."""
            async for tool in self.endpoint_manager.execute_tool_with_retry(self._list_tools):
                yield tool

        @self.server.call_tool()  # type: ignore
        async def handle_call_tool(
            name: str, arguments: dict[str, Any] | None
        ) -> AsyncGenerator[TextContent | ImageContent, None]:
            """Handle tool call request."""
            async for result in self.endpoint_manager.execute_tool_with_retry(
                lambda endpoint: self._call_tool(endpoint, name, arguments)
            ):
                yield result

    async def _list_tools(self, endpoint: str) -> AsyncGenerator[Tool, None]:
        """List available tools from IDE."""
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{endpoint}/mcp/list_tools') as response:
                if response.status == 404:
                    raise RuntimeError('No tools available')
                if not response.ok:
                    raise RuntimeError(f'Failed to list tools: {response.status} {response.reason}')

                data = await response.json()
                for tool_data in data['tools']:
                    yield Tool(**tool_data)

    async def _call_tool(
        self, endpoint: str, name: str, arguments: dict[str, Any] | None
    ) -> AsyncGenerator[TextContent | ImageContent, None]:
        """Call a tool on the IDE."""
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{endpoint}/mcp/call_tool', json={'name': name, 'arguments': arguments or {}}
            ) as response:
                if response.status == 404:
                    raise RuntimeError('Failed to call tool: Unknown tool')
                if response.status == 500:
                    raise RuntimeError('Failed to call tool: Tool execution failed')
                if not response.ok:
                    raise RuntimeError(f'Failed to call tool: {response.status} {response.reason}')

                data = await response.json()
                for content in data['content']:
                    if content['type'] == 'text':
                        yield TextContent(type='text', text=content['text'])
                    elif content['type'] == 'image':
                        yield ImageContent(type='image', data=content['data'], mimeType=content['mimeType'])

    def _on_tools_changed(self) -> None:
        """Handle tools list changes."""
        try:
            logger.info('Sending tools changed notification')
            self.server.notification({'method': 'notifications/tools/list_changed'})
        except Exception:
            logger.error('Failed to send tools changed notification', exc_info=True)

    async def shutdown(self) -> None:
        """Optional shutdown cleanup."""
        logger.info('Server shutting down gracefully...')
        # Add cleanup logic here as needed:
        # - Closing database connections
        # - Stopping background tasks
        logger.info('Server shutdown complete.')

    async def run(self) -> None:
        logger.info(f'Starting MCP JetBrains Proxy v{__version__}')

        async with anyio.create_task_group() as tg, mcp.server.stdio.stdio_server() as (read_stream, write_stream):
            with anyio.open_signal_receiver(signal.SIGINT, signal.SIGTERM) as signals:

                async def cancel_on_signal():
                    async for sig in signals:
                        logger.info(f'Received signal {sig.name}, cancelling tasks...')
                        tg.cancel_scope.cancel()
                        break

                tg.start_soon(cancel_on_signal)

                logger.info('Server running with stdio transport')
                try:
                    await self.server.run(
                        read_stream,
                        write_stream,
                        InitializationOptions(
                            server_name='jetbrains/proxy',
                            server_version=__version__,
                            capabilities=self.server.get_capabilities(
                                notification_options=NotificationOptions(tools_changed=True),
                                experimental_capabilities={},
                            ),
                        ),
                    )
                except anyio.get_cancelled_exc_class():
                    logger.info('Cancellation requested, initiating graceful shutdown...')
                    # Instead of calling shutdown here, re-raise so it’s caught in the finally block
                    # raise KeyboardInterrupt() from exc
                    await self.shutdown()
                    os._exit(0)

                except Exception as exc:
                    logger.error(f'Unexpected error in server.run: {exc}', exc_info=True)
                    # Let the finally block handle the shutdown below
                    os._exit(1)


def main() -> None:
    """Run the MCP server."""
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')
    server = MCPServer()

    # There's no need to handle KeyboardInterrupt here
    # because we forcibly exit inside server.run().
    anyio.run(server.run)

    # By the time we get here, either the server completed normally (no signals)
    # or `os._exit(...)` was already called for shutdown/errors.
    # So this code only runs if server.run() returned *without* being cancelled.
    logger.info('Normal exit from main() — no Ctrl-C was pressed.')
    os._exit(0)
