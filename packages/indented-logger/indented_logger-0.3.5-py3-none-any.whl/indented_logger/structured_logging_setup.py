import logging
import sys
import structlog

from structlog.stdlib import ProcessorFormatter

# Import your custom processors
from .structured_processors import (
    request_id_var,
    user_id_var,
    add_context_vars,
    add_global_fields,
    IndentationProcessor,
    FunctionNameProcessor
)

def set_request_context(request_id, user_id):
    """
    Store the request_id and user_id in context variables.
    """
    request_id_var.set(request_id)
    user_id_var.set(user_id)

def setup_structured_logging(level=logging.INFO, indent_spaces=4):
    """
    Configure structured logging using structlog with JSON output,
    including indentation and contextvars (request_id, user_id).
    """

    processors = [
        add_global_fields,                     # Adds global fields (app_version, env)
        add_context_vars,                      # Adds request_id, user_id from contextvars
        structlog.processors.TimeStamper(fmt="ISO", utc=True),
        FunctionNameProcessor(),
        IndentationProcessor(indent_spaces=indent_spaces),
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]

    # Configure structlog
    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    # The final output will be JSON
    formatter = ProcessorFormatter(
        processor=structlog.processors.JSONRenderer(sort_keys=True),
         foreign_pre_chain=[
        # We want these to run for foreign (i.e. stdlib) logs, too:
        add_global_fields,
        add_context_vars,
        structlog.processors.TimeStamper(fmt="ISO", utc=True),
        FunctionNameProcessor(),
        IndentationProcessor(indent_spaces=indent_spaces),
        # Note: wrap_for_formatter is NOT put here; it’s already in your structlog.configure(...) chain
    ],
    )

    # Create a handler that outputs to stdout
    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    # Replace any existing handlers on the root logger
    root_logger = logging.getLogger()
    root_logger.handlers = [handler]
    root_logger.setLevel(level)

    from .log_indent_switcher import use_structured_log_indent
    use_structured_log_indent()
