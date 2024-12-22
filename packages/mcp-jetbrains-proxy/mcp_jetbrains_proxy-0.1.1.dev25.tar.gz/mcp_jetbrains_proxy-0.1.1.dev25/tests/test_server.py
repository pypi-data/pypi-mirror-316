"""Tests for MCP server implementation."""

import asyncio
import logging
import time

import aiohttp
import pytest
from mcp.server import NotificationOptions
from mcp.server.models import InitializationOptions
from mcp.types import ServerCapabilities, ToolsCapability

from mcp_jetbrains_proxy import __version__
from mcp_jetbrains_proxy.endpoint import EndpointManager, PortRange
from mcp_jetbrains_proxy.server import MCPServer
from tests.conftest import TEST_PORT_END, TEST_PORT_START

logger = logging.getLogger(__name__)


@pytest.mark.asyncio
async def test_server_initialization(mock_mcp_client):
    """Test server initialization."""
    server = MCPServer()
    server.endpoint_manager = EndpointManager(port_range=PortRange(start=TEST_PORT_START, end=TEST_PORT_END))

    # Initialize client and server
    await mock_mcp_client.initialize(
        InitializationOptions(
            server_name='jetbrains/proxy',
            server_version=__version__,
            capabilities=ServerCapabilities(tools=ToolsCapability(listChanged=True)),
        )
    )

    # Patch server notification to use mock client
    logger = logging.getLogger(__name__)

    def mock_notification(params):
        logger.info(f'Server sending notification: {params}')
        if mock_mcp_client.tools_changed_callback:
            logger.info('Calling tools changed callback')
            mock_mcp_client.tools_changed_callback(params)
        else:
            logger.warning('No tools changed callback registered')

    server.server.notification = mock_notification

    # Create server with tools changed callback
    server.endpoint_manager._tools_changed_callback = lambda: mock_notification(
        {'method': 'notifications/tools/list_changed'}
    )

    # Verify capabilities
    capabilities = server.server.get_capabilities(
        notification_options=NotificationOptions(tools_changed=True), experimental_capabilities={}
    )

    assert capabilities.tools.listChanged is True


@pytest.mark.asyncio
async def test_list_tools(mock_ide_server, mock_mcp_client):
    """Test tools listing."""
    server = MCPServer()
    server.endpoint_manager = EndpointManager(port_range=PortRange(start=TEST_PORT_START, end=TEST_PORT_END))

    # Initialize client and server
    await mock_mcp_client.initialize(
        InitializationOptions(
            server_name='jetbrains/proxy',
            server_version=__version__,
            capabilities=ServerCapabilities(tools=ToolsCapability(listChanged=True)),
        )
    )

    # Patch server notification to use mock client
    logger = logging.getLogger(__name__)

    def mock_notification(params):
        logger.info(f'Server sending notification: {params}')
        if mock_mcp_client.tools_changed_callback:
            logger.info('Calling tools changed callback')
            mock_mcp_client.tools_changed_callback(params)
        else:
            logger.warning('No tools changed callback registered')

    server.server.notification = mock_notification

    # Create server with tools changed callback
    server.endpoint_manager._tools_changed_callback = lambda: mock_notification(
        {'method': 'notifications/tools/list_changed'}
    )

    # Get tools list
    tools = await server._list_tools(f'http://localhost:{mock_ide_server["port"]}')

    assert len(tools) == 1
    assert tools[0].name == 'test-tool'
    assert tools[0].description == 'A test tool'
    assert tools[0].inputSchema['properties']['arg1']['type'] == 'string'
    assert tools[0].inputSchema['properties']['arg1']['description'] == 'Test argument'
    assert tools[0].inputSchema['required'] == ['arg1']


@pytest.mark.asyncio
async def test_call_tool(mock_ide_server, mock_mcp_client):
    """Test tool calling."""
    server = MCPServer()
    server.endpoint_manager = EndpointManager(port_range=PortRange(start=TEST_PORT_START, end=TEST_PORT_END))

    # Initialize client and server
    await mock_mcp_client.initialize(
        InitializationOptions(
            server_name='jetbrains/proxy',
            server_version=__version__,
            capabilities=ServerCapabilities(tools=ToolsCapability(listChanged=True)),
        )
    )

    # Patch server notification to use mock client
    logger = logging.getLogger(__name__)

    def mock_notification(params):
        logger.info(f'Server sending notification: {params}')
        if mock_mcp_client.tools_changed_callback:
            logger.info('Calling tools changed callback')
            mock_mcp_client.tools_changed_callback(params)
        else:
            logger.warning('No tools changed callback registered')

    server.server.notification = mock_notification

    # Create server with tools changed callback
    server.endpoint_manager._tools_changed_callback = lambda: mock_notification(
        {'method': 'notifications/tools/list_changed'}
    )

    # Call tool
    content = await server._call_tool(f'http://localhost:{mock_ide_server["port"]}', 'test-tool', {'arg1': 'test'})

    assert len(content) == 1
    assert content[0].type == 'text'
    assert content[0].text.startswith('Tool called with args:')


@pytest.mark.asyncio
async def test_tools_changed_notification(mock_mcp_client, mock_ide_server):
    """Test tools changed notification."""
    server = MCPServer()

    # Initialize client and server
    await mock_mcp_client.initialize(
        InitializationOptions(
            server_name='jetbrains/proxy',
            server_version=__version__,
            capabilities=ServerCapabilities(tools=ToolsCapability(listChanged=True)),
        )
    )

    # Patch server notification to use mock client
    logger = logging.getLogger(__name__)

    def mock_notification(params):
        logger.info(f'Server sending notification: {params}')
        if mock_mcp_client.tools_changed_callback:
            logger.info('Calling tools changed callback')
            mock_mcp_client.tools_changed_callback(params)
        else:
            logger.warning('No tools changed callback registered')

    server.server.notification = mock_notification

    # Create server with tools changed callback
    server.endpoint_manager._tools_changed_callback = lambda: mock_notification(
        {'method': 'notifications/tools/list_changed'}
    )

    # Mock IDE server should send tools changed notification
    notification_received = asyncio.Event()

    def on_notification(params):
        logger.info(f'Received notification: {params}')
        if params.get('method') == 'notifications/tools/list_changed':
            logger.info('Setting notification received event')
            notification_received.set()
        else:
            logger.info(f"Ignoring notification with method: {params.get('method')}")

    mock_mcp_client.on_notification('notifications/tools/list_changed', on_notification)

    # Create new app with updated tools list
    app = aiohttp.web.Application()

    async def list_tools(_):
        """List available tools."""
        return aiohttp.web.json_response(
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
        if data.get('name') == 'error-tool':
            return aiohttp.web.Response(status=500, text='Tool execution failed')

        return aiohttp.web.json_response(
            {'content': [{'type': 'text', 'text': f'Tool called with args: {data["arguments"]}'}]}
        )

    app.router.add_get('/mcp/list_tools', list_tools)
    app.router.add_post('/mcp/call_tool', handle_call_tool)

    # Get initial tools list
    tools = await server.endpoint_manager.execute_tool_with_retry(lambda endpoint: server._list_tools(endpoint))

    assert len(tools) > 0
    assert tools[0].name == 'test-tool'

    # Stop old server
    await mock_ide_server['runner'].cleanup()

    # Create new app with different tools
    new_app = aiohttp.web.Application()

    async def updated_list_tools(_):
        """Updated tools list handler."""
        return aiohttp.web.json_response(
            {
                'tools': [
                    {
                        'name': 'new-tool',
                        'description': 'A new test tool',
                        'inputSchema': {
                            'type': 'object',
                            'properties': {'arg1': {'type': 'string', 'description': 'Test argument'}},
                            'required': ['arg1'],
                        },
                    }
                ]
            }
        )

    new_app.router.add_get('/mcp/list_tools', updated_list_tools)
    new_app.router.add_post('/mcp/call_tool', handle_call_tool)

    # Start new server
    runner = aiohttp.web.AppRunner(new_app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, 'localhost', mock_ide_server['port'])
    await site.start()

    # Force endpoint manager to check again
    server.endpoint_manager._last_checked = 0
    server.endpoint_manager._endpoint = None

    # Get updated tools list, this should trigger notification
    updated_tools = await server.endpoint_manager.execute_tool_with_retry(lambda endpoint: server._list_tools(endpoint))

    assert len(updated_tools) > 0
    assert updated_tools[0].name == 'new-tool'

    # Wait for notification
    try:
        await asyncio.wait_for(notification_received.wait(), timeout=5)
    except asyncio.TimeoutError:
        pytest.fail('Tools changed notification not received')

    # Cleanup
    await runner.cleanup()


@pytest.mark.asyncio
async def test_invalid_tool_call(mock_ide_server, mock_mcp_client):
    """Test handling of invalid tool calls."""
    server = MCPServer()
    server.endpoint_manager = EndpointManager(port_range=PortRange(start=TEST_PORT_START, end=TEST_PORT_END))

    # Initialize client and server
    await mock_mcp_client.initialize(
        InitializationOptions(
            server_name='jetbrains/proxy',
            server_version=__version__,
            capabilities=ServerCapabilities(tools=ToolsCapability(listChanged=True)),
        )
    )

    # Patch server notification to use mock client
    logger = logging.getLogger(__name__)

    def mock_notification(params):
        logger.info(f'Server sending notification: {params}')
        if mock_mcp_client.tools_changed_callback:
            logger.info('Calling tools changed callback')
            mock_mcp_client.tools_changed_callback(params)
        else:
            logger.warning('No tools changed callback registered')

    server.server.notification = mock_notification

    # Create server with tools changed callback
    server.endpoint_manager._tools_changed_callback = lambda: mock_notification(
        {'method': 'notifications/tools/list_changed'}
    )

    # Call invalid tool
    with pytest.raises(RuntimeError, match='Failed to call tool: Unknown tool'):
        await server._call_tool(f'http://localhost:{mock_ide_server["port"]}', 'invalid-tool', {})


@pytest.mark.asyncio
async def test_tool_error_handling(mock_ide_server, mock_mcp_client):
    """Test handling of tool errors."""
    server = MCPServer()
    server.endpoint_manager = EndpointManager(
        port_range=PortRange(start=TEST_PORT_START, end=TEST_PORT_END),
        request_timeout=0.1,
        retry_delay=0.1,
        max_retry_attempts=2,
    )

    # Initialize client and server
    await mock_mcp_client.initialize(
        InitializationOptions(
            server_name='jetbrains/proxy',
            server_version=__version__,
            capabilities=ServerCapabilities(tools=ToolsCapability(listChanged=True)),
        )
    )

    # Patch server notification to use mock client
    logger = logging.getLogger(__name__)

    def mock_notification(params):
        logger.info(f'Server sending notification: {params}')
        if mock_mcp_client.tools_changed_callback:
            logger.info('Calling tools changed callback')
            mock_mcp_client.tools_changed_callback(params)
        else:
            logger.warning('No tools changed callback registered')

    server.server.notification = mock_notification

    # Create server with tools changed callback
    server.endpoint_manager._tools_changed_callback = lambda: mock_notification(
        {'method': 'notifications/tools/list_changed'}
    )

    # Call tool that will fail
    with pytest.raises(RuntimeError, match='Failed to call tool: Tool execution failed'):
        await server._call_tool(f'http://localhost:{mock_ide_server["port"]}', 'test-tool', {'arg1': 'fail'})


@pytest.mark.asyncio
async def test_concurrent_tool_calls(mock_ide_server, mock_mcp_client):
    """Test concurrent tool calls."""
    server = MCPServer()
    server.endpoint_manager = EndpointManager(port_range=PortRange(start=TEST_PORT_START, end=TEST_PORT_END))

    # Initialize client and server
    await mock_mcp_client.initialize(
        InitializationOptions(
            server_name='jetbrains/proxy',
            server_version=__version__,
            capabilities=ServerCapabilities(tools=ToolsCapability(listChanged=True)),
        )
    )

    # Patch server notification to use mock client
    logger = logging.getLogger(__name__)

    def mock_notification(params):
        logger.info(f'Server sending notification: {params}')
        if mock_mcp_client.tools_changed_callback:
            logger.info('Calling tools changed callback')
            mock_mcp_client.tools_changed_callback(params)
        else:
            logger.warning('No tools changed callback registered')

    server.server.notification = mock_notification

    # Create server with tools changed callback
    server.endpoint_manager._tools_changed_callback = lambda: mock_notification(
        {'method': 'notifications/tools/list_changed'}
    )

    # Make concurrent tool calls
    async def call_tool(i: int):
        content = await server._call_tool(
            f'http://localhost:{mock_ide_server["port"]}', 'test-tool', {'arg1': f'test{i}'}
        )
        return content

    tasks = [call_tool(i) for i in range(3)]
    results = await asyncio.gather(*tasks)

    for content in results:
        assert len(content) == 1
        assert content[0].type == 'text'
        assert content[0].text.startswith('Tool called with args:')


@pytest.mark.asyncio
async def test_server_shutdown(mock_ide_server, mock_mcp_client):
    """Test server shutdown."""
    server = MCPServer()
    server.endpoint_manager = EndpointManager(port_range=PortRange(start=TEST_PORT_START, end=TEST_PORT_END))

    # Initialize client and server
    await mock_mcp_client.initialize(
        InitializationOptions(
            server_name='jetbrains/proxy',
            server_version=__version__,
            capabilities=ServerCapabilities(tools=ToolsCapability(listChanged=True)),
        )
    )

    # Patch server notification to use mock client
    logger = logging.getLogger(__name__)

    def mock_notification(params):
        logger.info(f'Server sending notification: {params}')
        if mock_mcp_client.tools_changed_callback:
            logger.info('Calling tools changed callback')
            mock_mcp_client.tools_changed_callback(params)
        else:
            logger.warning('No tools changed callback registered')

    server.server.notification = mock_notification

    # Create server with tools changed callback
    server.endpoint_manager._tools_changed_callback = lambda: mock_notification(
        {'method': 'notifications/tools/list_changed'}
    )

    # Verify server is running
    tools = await server._list_tools(f'http://localhost:{mock_ide_server["port"]}')
    assert len(tools) == 1


@pytest.mark.asyncio
async def test_list_tools_error_handling(mock_ide_server):
    """Test error handling in list_tools."""
    server = MCPServer()

    # Clean up existing server
    await mock_ide_server['runner'].cleanup()

    # Create new app with 404 response
    app = aiohttp.web.Application()

    # Add health check endpoint that returns healthy
    async def health_check(_):
        return aiohttp.web.json_response({'tools': []})

    app.router.add_get('/mcp/list_tools', health_check)

    runner = aiohttp.web.AppRunner(app)
    await runner.setup()
    site = aiohttp.web.TCPSite(runner, 'localhost', mock_ide_server['port'])
    await site.start()

    # Set up a healthy endpoint first
    server.endpoint_manager._endpoint = f'http://localhost:{mock_ide_server["port"]}'
    server.endpoint_manager._last_checked = time.time()

    # Create a new app with 404 response
    app2 = aiohttp.web.Application()

    async def list_tools(_):
        return aiohttp.web.Response(status=404)

    app2.router.add_get('/mcp/list_tools', list_tools)

    runner2 = aiohttp.web.AppRunner(app2)
    await runner2.setup()
    site2 = aiohttp.web.TCPSite(runner2, 'localhost', mock_ide_server['port'])

    # Stop the first site and start the second one
    await site.stop()
    await site2.start()

    with pytest.raises(RuntimeError, match='No healthy endpoints found'):
        await server.endpoint_manager.execute_tool_with_retry(lambda endpoint: server._list_tools(endpoint))

    await runner.cleanup()
    await runner2.cleanup()


@pytest.mark.asyncio
async def test_tools_changed_notification_error(mock_mcp_client):
    """Test error handling in tools changed notification."""
    server = MCPServer()

    # Initialize client and server
    await mock_mcp_client.initialize(
        InitializationOptions(
            server_name='jetbrains/proxy',
            server_version=__version__,
            capabilities=ServerCapabilities(tools=ToolsCapability(listChanged=True)),
        )
    )

    # Patch server notification to raise an error
    def mock_notification(params):
        raise RuntimeError('Failed to send notification')

    server.server.notification = mock_notification

    # Trigger notification and ensure it doesn't raise
    server._on_tools_changed()  # Should log error but not raise
