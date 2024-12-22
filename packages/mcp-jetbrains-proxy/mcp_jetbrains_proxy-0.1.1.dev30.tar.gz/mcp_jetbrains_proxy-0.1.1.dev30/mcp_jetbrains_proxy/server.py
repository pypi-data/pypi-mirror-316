import argparse
import logging
import os
import signal
from typing import Any

import aiohttp
import anyio
import mcp.server.stdio
from mcp.server import NotificationOptions, Server
from mcp.server.models import InitializationOptions
from mcp.types import TextContent, Tool

from . import __version__, server_name
from .endpoint import EndpointManager, PortRange
from .logging import MCPLogHandler

logger = logging.getLogger(__name__)

PORT_RANGE_START = os.environ.get('PORT_RANGE_START', 63342)
PORT_RANGE_END = os.environ.get('PORT_RANGE_END', 63352)


class MCPServer:
    """MCP server for JetBrains IDE proxy."""

    def __init__(self, mcp_logging: bool = True) -> None:
        """Initialize MCP server."""
        self.server = Server(server_name)
        self.endpoint_manager = EndpointManager(
            port_range=PortRange(start=PORT_RANGE_START, end=PORT_RANGE_END),
            tools_changed_callback=self._on_tools_changed,
        )

        # Set up MCP logging handler
        if mcp_logging:
            log_handler = MCPLogHandler(self.server)
            log_handler.setFormatter(logging.Formatter('%(message)s'))
            logger.addHandler(log_handler)

        self._setup_handlers()

    def _setup_handlers(self) -> None:
        """Set up MCP request handlers."""

        @self.server.list_tools()  # type: ignore
        async def handle_list_tools() -> list[Tool]:
            """Handle list tools request."""
            # TODO: Add better error handling
            return await self.endpoint_manager.execute_tool_with_retry(self._list_tools)

        @self.server.call_tool()  # type: ignore
        async def handle_call_tool(name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
            """Handle tool call request."""
            # TODO: Add better error handling
            return await self.endpoint_manager.execute_tool_with_retry(
                lambda endpoint: self._call_tool(endpoint, name, arguments)
            )

    async def _list_tools(self, endpoint: str) -> list[Tool]:
        """List available tools from IDE."""
        logger.info(f'Listing tools on endpoint {endpoint}')
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{endpoint}/mcp/list_tools') as response:
                if response.status == 404:
                    raise RuntimeError('No tools available')
                if not response.ok:
                    raise RuntimeError(f'Failed to list tools: {response.status} {response.reason}')

                data = await response.json()
                return [Tool(**tool_data) for tool_data in data]

    async def _call_tool(self, endpoint: str, name: str, arguments: dict[str, Any] | None) -> list[TextContent]:
        """Call a tool on the IDE."""
        logger.info(f'Calling tool {name} on endpoint {endpoint}')
        async with aiohttp.ClientSession() as session:
            async with session.post(
                f'{endpoint}/mcp/{name}',
                json=arguments or {},
            ) as response:
                if response.status == 404:
                    raise RuntimeError('Failed to call tool: Unknown tool')
                if response.status == 500:
                    raise RuntimeError('Failed to call tool: Tool execution failed')
                if not response.ok:
                    raise RuntimeError(f'Failed to call tool: {response.status} {response.reason}')

                data = await response.json()
                status = data.get('status')
                error = data.get('error')
                text = status if status is not None else error
                return [TextContent(type='text', text=text)] if text is not None else []

    def _on_tools_changed(self) -> None:
        """Handle tools list changes."""
        logger.info('Sending tools changed notification')
        try:
            self.server.notification({'method': 'notifications/tools/list_changed'})
        except Exception:
            logger.error('Failed to send tools changed notification', exc_info=True)

    async def shutdown(self) -> None:
        """Optional shutdown cleanup."""
        logger.info('Server shutting down gracefully...')
        # Add cleanup logic here as needed:
        # - Closing connections
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
                            server_name=server_name,
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
                    logger.error(f'Unexpected error in server.run: {exc}')
                    # Let the finally block handle the shutdown below
                    os._exit(1)


def main() -> None:
    """Run the MCP server."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='MCP JetBrains Proxy Server')
    parser.add_argument('--version', action='version', version=f'MCP JetBrains Proxy v{__version__}')
    parser.add_argument('--no-stdout', action='store_true', help='Disable logging to stdout')
    parser.add_argument('--test', action='store_true', help='Test mode')
    args = parser.parse_args()

    # Configure logging with stdout by default
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

    # Remove stdout handler if --no-stdout is specified
    if args.no_stdout:
        root_logger = logging.getLogger()
        for handler in root_logger.handlers[:]:
            if isinstance(handler, logging.StreamHandler):
                root_logger.removeHandler(handler)

    if args.test:
        logger.info('Running in test mode')
        server = MCPServer()

        async def handle_list_tools() -> None:
            logger.info('Listing tools...')
            tools = await server.endpoint_manager.execute_tool_with_retry(server._list_tools)
            logger.info(tools)

        anyio.run(handle_list_tools)
        return

    server = MCPServer()

    # There's no need to handle KeyboardInterrupt here
    # because we forcibly exit inside server.run().
    anyio.run(server.run)

    # By the time we get here, either the server completed normally (no signals)
    # or `os._exit(...)` was already called for shutdown/errors.
    # So this code only runs if server.run() returned *without* being cancelled.
    logger.info('Exiting...')
    os._exit(0)
