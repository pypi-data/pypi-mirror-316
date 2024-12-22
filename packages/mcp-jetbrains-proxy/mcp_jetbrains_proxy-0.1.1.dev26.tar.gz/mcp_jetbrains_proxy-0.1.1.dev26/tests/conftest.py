"""Test configuration and fixtures."""

import logging
from typing import Callable
from unittest.mock import AsyncMock

import mcp.types as types
import pytest
import pytest_asyncio
from aiohttp import web
from mcp.server.models import InitializationOptions

# Use the same port range as the implementation
TEST_PORT_START = 63342
TEST_PORT_END = 63352


@pytest.fixture
async def mock_ide_server():
    """Create a mock IDE server for testing."""
    app = web.Application()

    async def handle_list_tools(request):
        """Handle /mcp/list_tools endpoint."""
        return web.json_response(
            {
                'tools': [
                    {
                        'name': 'test-tool',
                        'description': 'A test tool',
                        'inputSchema': {
                            'type': 'object',
                            'properties': {'arg1': {'type': 'string', 'description': 'Test argument'}},
                            'required': ['arg1'],
                        },
                    }
                ]
            }
        )

    async def handle_call_tool(request):
        """Handle tool call."""
        data = await request.json()
        if data.get('arg1') == 'fail':
            return web.Response(status=500, text='Tool execution failed')

        return web.json_response({'status': f'Tool called with args: {data}'})

    app.router.add_get('/api/mcp/list_tools', handle_list_tools)
    app.router.add_post('/api/mcp/test-tool', handle_call_tool)

    # Find an available port in the range
    for port in range(TEST_PORT_START, TEST_PORT_END + 1):
        try:
            runner = web.AppRunner(app)
            await runner.setup()
            site = web.TCPSite(runner, 'localhost', port)
            await site.start()
            yield {'app': app, 'port': port, 'runner': runner}
            await runner.cleanup()
            break
        except OSError:
            await runner.cleanup()
            continue


@pytest_asyncio.fixture
async def mock_mcp_client():
    """Create a mock MCP client that can interact with our server."""
    logger = logging.getLogger(__name__)

    class MockMCPClient:
        def __init__(self):
            self.read_stream = AsyncMock()
            self.write_stream = AsyncMock()
            self.tools_changed_callback = None
            self.initialization_options = None

        async def initialize(self, initialization_options: InitializationOptions):
            """Initialize client with given options."""
            self.initialization_options = initialization_options

        async def list_tools(self):
            """List available tools."""
            return [
                types.Tool(
                    name='test-tool',
                    description='A test tool',
                    inputSchema={
                        'type': 'object',
                        'properties': {'arg1': {'type': 'string', 'description': 'Test argument'}},
                        'required': ['arg1'],
                    },
                )
            ]

        async def call_tool(self, name: str, arguments: dict):
            """Call a tool."""
            if name == 'invalid-tool':
                raise RuntimeError('Unknown tool')
            elif arguments.get('arg1') == 'fail':
                raise RuntimeError('Tool execution failed')

            return [types.TextContent(type='text', text=f'Tool called with args: {arguments}')]

        def on_notification(self, method: str, handler: Callable[[dict], None]):
            """Register notification handler."""
            logger.info(f'Registering notification handler for method: {method}')
            if method == 'notifications/tools/list_changed':
                logger.info('Setting tools changed callback')
                self.tools_changed_callback = lambda params: handler(params)
                logger.info('Tools changed callback set successfully')
            else:
                logger.info(f'Ignoring notification method: {method}')

        async def simulate_tools_changed(self):
            """Simulate tools changed notification."""
            logger.info('Simulating tools changed notification')
            if self.tools_changed_callback:
                logger.info('Calling tools changed callback')
                await self.tools_changed_callback({'tools': []})
            else:
                logger.info('No tools changed callback registered')

    client = MockMCPClient()
    yield client
