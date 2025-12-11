"""
SIMBA Backend - Logging Utility

Structured logging using structlog.
"""

import logging
import sys
from typing import Any

import structlog
from app.config import settings


def setup_logging() -> None:
    """Configure structured logging"""

    # Configure standard logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, settings.LOG_LEVEL.upper()),
    )

    # Configure structlog
    structlog.configure(
        processors=[
            structlog.contextvars.merge_contextvars,
            structlog.stdlib.filter_by_level,
            structlog.stdlib.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.processors.StackInfoRenderer(),
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.JSONRenderer()
            if not settings.DEBUG
            else structlog.dev.ConsoleRenderer(),
        ],
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


# Create logger instance
logger = structlog.get_logger()

# Setup logging on import
setup_logging()


def log_exception(exc: Exception, **kwargs: Any) -> None:
    """Log exception with context"""
    logger.error(
        "Exception occurred",
        exc_info=exc,
        exception_type=type(exc).__name__,
        **kwargs,
    )


def log_api_request(
    method: str,
    path: str,
    status_code: int,
    duration_ms: float,
    **kwargs: Any,
) -> None:
    """Log API request"""
    logger.info(
        "API Request",
        method=method,
        path=path,
        status_code=status_code,
        duration_ms=duration_ms,
        **kwargs,
    )


def log_tool_execution(
    tool_name: str,
    success: bool,
    duration_ms: float,
    **kwargs: Any,
) -> None:
    """Log tool execution"""
    logger.info(
        "Tool Execution",
        tool_name=tool_name,
        success=success,
        duration_ms=duration_ms,
        **kwargs,
    )
