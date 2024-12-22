import logging

__all__ = ['MCPLogHandler']


class MCPLogHandler(logging.Handler):
    """Custom logging handler that forwards logs to MCP client."""

    def __init__(self, server):
        """Initialize the handler with MCP server instance."""
        super().__init__()
        self.server = server

    def emit(self, record):
        """Emit a log record by sending it to the MCP client."""
        try:
            # Only send if we have an active session
            if hasattr(self.server, 'request_context') and self.server.request_context is not None:
                self.server.request_context.session.send_log_message(
                    level={
                        logging.DEBUG: 'debug',
                        logging.INFO: 'info',
                        logging.WARNING: 'warning',
                        logging.ERROR: 'error',
                        logging.CRITICAL: 'error',
                    }.get(record.levelno, 'info'),
                    data=self.format(record),
                )
        except Exception:
            # Avoid infinite recursion if logging fails
            pass
