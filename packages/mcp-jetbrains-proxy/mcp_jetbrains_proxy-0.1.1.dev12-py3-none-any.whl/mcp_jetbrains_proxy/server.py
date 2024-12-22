"""MCP server implementation for JetBrains IDE proxy."""

import asyncio
import logging
from typing import Any, AsyncGenerator

import aiohttp
from mcp.server import Server
from mcp.types import ImageContent, TextContent, Tool

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
        """List available tools from IDE.

        Args:
            endpoint: IDE endpoint URL

        Yields:
            Available tools
        """
        async with aiohttp.ClientSession() as session:
            async with session.get(f'{endpoint}/mcp/list_tools') as response:
                if response.status == 404:
                    raise RuntimeError('No tools available')
                if not response.ok:
                    raise RuntimeError(f'Failed to list tools: {response.status} {response.reason}')

                data = await response.json()
                for tool in data['tools']:
                    yield Tool(**tool)

    async def _call_tool(
        self, endpoint: str, name: str, arguments: dict[str, Any] | None
    ) -> AsyncGenerator[TextContent | ImageContent, None]:
        """Call a tool on the IDE.

        Args:
            endpoint: IDE endpoint URL
            name: Tool name
            arguments: Tool arguments

        Yields:
            Tool results as text or image content
        """
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
            logger.info('Tools changed notification sent successfully')
        except Exception:
            logger.error('Failed to send tools changed notification', exc_info=True)

    def run(self) -> None:
        """Run the MCP server."""
        logger.info('Starting MCP server')
        asyncio.run(
            Server.stdio_server(self.server)  # type: ignore
        )


def main() -> None:
    """Run the MCP server."""
    logging.basicConfig(level=logging.INFO, format='[%(levelname)s] %(message)s')

    server = MCPServer()
    server.run()
