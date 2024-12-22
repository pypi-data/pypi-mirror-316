"""IDE endpoint discovery and management."""

import asyncio
import logging
import os
import time
from dataclasses import dataclass
from typing import Any, Awaitable, Callable, TypeVar

import aiohttp

logger = logging.getLogger(__name__)


@dataclass
class PortRange:
    """Port range for IDE endpoint discovery."""

    start: int
    end: int


T = TypeVar('T')


class EndpointManager:
    """Manages IDE endpoint discovery and health checks."""

    def __init__(
        self,
        port_range: PortRange | None = None,
        check_interval: float = 60.0,
        request_timeout: float = 5.0,
        retry_delay: float = 1.0,
        max_retry_attempts: int = 3,
        tools_changed_callback: Callable[[], None] | None = None,
    ):
        """Initialize endpoint manager.

        Args:
            port_range: Port range to scan for IDE endpoints
            check_interval: Interval between endpoint health checks in seconds
            request_timeout: Timeout for endpoint requests in seconds
            retry_delay: Delay between retry attempts in seconds
            max_retry_attempts: Maximum number of retry attempts
            tools_changed_callback: Optional callback for tools list changes
        """
        self._port_range = port_range or PortRange(start=63342, end=63352)
        self._check_interval = check_interval
        self._request_timeout = request_timeout
        self._retry_delay = retry_delay
        self._max_retry_attempts = max_retry_attempts
        self._tools_changed_callback = tools_changed_callback

        self._endpoint: str | None = None
        self._last_checked = 0.0
        self._lock = asyncio.Lock()
        self._previous_tools_response: str | None = None

    async def __aenter__(self) -> 'EndpointManager':
        """Enter context manager."""
        return self

    async def __aexit__(self, exc_type: type[BaseException] | None, exc_val: BaseException | None, exc_tb: Any) -> None:
        """Exit context manager."""
        pass

    async def get_endpoint(self) -> str:
        """Get a healthy IDE endpoint.

        Returns:
            IDE endpoint URL

        Raises:
            RuntimeError: If no healthy endpoints found
        """
        now = time.time()

        # Return cached endpoint if still valid
        if self._endpoint is not None and now - self._last_checked < self._check_interval:
            logger.info(f'Using cached endpoint {self._endpoint}')
            return self._endpoint

        logger.info('Finding healthy endpoint')

        # Acquire lock to prevent concurrent discovery
        async with self._lock:
            # Check again in case another task found endpoint
            if self._endpoint is not None and now - self._last_checked < self._check_interval:
                logger.info(f'Using cached endpoint {self._endpoint}')
                return self._endpoint

            # Try environment variable first
            if 'IDE_PORT' in os.environ:
                port = int(os.environ['IDE_PORT'])
                endpoint = f'http://localhost:{port}'
                try:
                    await self._check_endpoint(endpoint)
                    self._endpoint = endpoint
                    self._last_checked = now
                    return endpoint
                except Exception:
                    logger.error(f'IDE_PORT={port} is not responding')

            # Scan port range
            async with aiohttp.ClientSession():
                for port in range(self._port_range.start, self._port_range.end + 1):
                    endpoint = f'http://localhost:{port}'
                    try:
                        await self._check_endpoint(endpoint)
                        self._endpoint = endpoint
                        self._last_checked = now
                        logger.info(f'Found healthy endpoint {endpoint}')
                        return endpoint
                    except Exception:
                        logger.error(f'Endpoint {endpoint} returned status 404')

            raise RuntimeError('No healthy endpoints found')

    async def _check_endpoint(self, endpoint: str) -> None:
        """Check if endpoint is healthy and detect tools changes.

        Args:
            endpoint: Endpoint URL to check

        Raises:
            Exception: If endpoint is not healthy
        """
        logger.info(f'Checking endpoint {endpoint}')

        async with aiohttp.ClientSession() as session:
            async with session.get(
                f'{endpoint}/mcp/list_tools',
                timeout=float(self._request_timeout),  # type: ignore
            ) as response:
                if not response.ok:
                    logger.error(f'Endpoint {endpoint} returned status {response.status}')
                    raise RuntimeError(f'Endpoint health check failed: {response.status}')

                # Check for tools changes
                current_response = await response.text()
                logger.info(f'Current tools response: {current_response}')
                logger.info(f'Previous tools response: {self._previous_tools_response}')

                if (
                    self._previous_tools_response is not None
                    and current_response != self._previous_tools_response
                    and self._tools_changed_callback is not None
                ):
                    logger.info('Tools list changed, sending notification')
                    logger.info(f'Current tools: {current_response}')
                    logger.info(f'Previous tools: {self._previous_tools_response}')
                    self._tools_changed_callback()

                # Always update previous response after checking for changes
                self._previous_tools_response = current_response

    async def execute_tool_with_retry(self, tool_call: Callable[[str], Awaitable[T]]) -> T:
        """Execute a tool call with automatic retries.

        Args:
            tool_call: Async function that takes endpoint URL and returns result

        Returns:
            Tool call result

        Raises:
            RuntimeError: If all retries failed
        """
        for attempt in range(1, self._max_retry_attempts + 1):
            try:
                endpoint = await self.get_endpoint()
                logger.info(
                    f'Executing tool call on endpoint {endpoint} ' f'(attempt {attempt}/{self._max_retry_attempts})'
                )
                return await tool_call(endpoint)
            except Exception as e:
                logger.error(f'Tool call failed on attempt {attempt}/{self._max_retry_attempts}', exc_info=True)
                if attempt == self._max_retry_attempts:
                    if isinstance(e, RuntimeError):
                        raise e
                    raise RuntimeError(str(e)) from e
                await asyncio.sleep(self._retry_delay)
                # Clear cached endpoint to force rediscovery
                self._endpoint = None
