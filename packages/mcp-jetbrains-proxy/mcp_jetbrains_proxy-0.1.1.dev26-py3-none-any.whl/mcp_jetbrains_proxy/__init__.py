"""MCP JetBrains Proxy - A proxy between LLM and MCP server within JetBrains IDE."""

try:
    from ._version import __version__, __version_tuple__
except ImportError:
    __version__ = '0.0.0'
    __version_tuple__ = (0, 0, 0)
