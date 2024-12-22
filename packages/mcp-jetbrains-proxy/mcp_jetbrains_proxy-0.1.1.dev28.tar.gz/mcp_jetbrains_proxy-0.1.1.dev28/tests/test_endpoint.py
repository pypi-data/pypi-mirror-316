"""Tests for IDE endpoint discovery and management."""

import asyncio
import logging
from unittest.mock import patch

import aiohttp
import pytest
from aiohttp import web

from mcp_jetbrains_proxy.endpoint import EndpointManager

logger = logging.getLogger(__name__)

TEST_PORT_START = 63342
TEST_PORT_END = 63352


@pytest.mark.asyncio
async def test_endpoint_discovery(mock_ide_server):
    """Test IDE endpoint discovery."""
    async with EndpointManager() as manager:
        endpoint = await manager.get_endpoint()
        assert endpoint == f'http://localhost:{mock_ide_server["port"]}/api'


@pytest.mark.asyncio
async def test_endpoint_caching(mock_ide_server):
    """Test endpoint caching behavior."""
    async with EndpointManager(check_interval=1.0) as manager:
        # First call should discover endpoint
        endpoint1 = await manager.get_endpoint()
        assert endpoint1 == f'http://localhost:{mock_ide_server["port"]}/api'

        # Second call should return cached endpoint
        endpoint2 = await manager.get_endpoint()
        assert endpoint2 == endpoint1


@pytest.mark.asyncio
async def test_endpoint_retry_on_failure(mock_ide_server):
    """Test retry behavior on endpoint failure."""
    async with EndpointManager(
        request_timeout=0.1,  # Short timeout for faster test
        retry_delay=0.1,  # Short delay between retries
        max_retry_attempts=2,  # Only try twice
    ) as manager:
        # First ensure we have a healthy endpoint
        endpoint = await manager.get_endpoint()
        assert endpoint == f'http://localhost:{mock_ide_server["port"]}/api'

        # Now test the failing tool call
        async def failing_tool_call(_):
            raise aiohttp.ClientError('Always fails')

        with pytest.raises(RuntimeError, match='Always fails'):
            await manager.execute_tool_with_retry(failing_tool_call)


@pytest.mark.asyncio
async def test_endpoint_max_retries(mock_ide_server):
    """Test max retries behavior."""
    async with EndpointManager(
        request_timeout=0.1,  # Short timeout for faster test
        retry_delay=0.1,  # Short delay between retries
        max_retry_attempts=2,  # Only try twice
    ) as manager:
        # First ensure we have a healthy endpoint
        endpoint = await manager.get_endpoint()
        assert endpoint == f'http://localhost:{mock_ide_server["port"]}/api'

        async def failing_tool_call(_):
            raise aiohttp.ClientError('Always fails')

        # Set a timeout for the entire operation
        async with asyncio.timeout(1.0):  # 1 second timeout
            with pytest.raises(RuntimeError, match='Always fails'):
                await manager.execute_tool_with_retry(failing_tool_call)


@pytest.mark.asyncio
async def test_endpoint_environment_override(mock_ide_server):
    """Test IDE_PORT environment variable override."""
    with patch.dict('os.environ', {'IDE_PORT': str(mock_ide_server['port'])}):
        async with EndpointManager() as manager:
            endpoint = await manager.get_endpoint()
            assert endpoint == f'http://localhost:{mock_ide_server["port"]}/api'


@pytest.mark.asyncio
async def test_endpoint_health_check():
    """Test endpoint health check."""
    async with EndpointManager(check_interval=0.1) as manager:
        # Should fail initially
        with pytest.raises(RuntimeError, match='No healthy endpoints found'):
            await manager.get_endpoint()

        # Start mock server
        app = web.Application()

        async def list_tools(_):
            return web.json_response([])

        app.router.add_get('/api/mcp/list_tools', list_tools)
        runner = web.AppRunner(app)
        await runner.setup()

        # Find available port
        port = TEST_PORT_START
        while port <= TEST_PORT_END:
            try:
                site = web.TCPSite(runner, 'localhost', port)
                await site.start()
                break
            except OSError:
                port += 1
                if port > TEST_PORT_END:
                    pytest.fail('No available ports')

        try:
            # Should succeed after endpoint becomes available
            endpoint = await manager.get_endpoint()
            assert endpoint == f'http://localhost:{port}/api'
        finally:
            await runner.cleanup()


@pytest.mark.asyncio
async def test_concurrent_health_checks():
    """Test concurrent health checks."""
    async with EndpointManager(check_interval=0.1) as manager:
        # Run multiple health checks concurrently
        async def check_endpoint():
            try:
                await manager.get_endpoint()
            except RuntimeError:
                pass  # Expected when no endpoints are available

        await asyncio.gather(*[check_endpoint() for _ in range(5)])
