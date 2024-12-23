# structured_logging_setup.py

import logging
import sys
import structlog

from .structured_processors import (
    request_id_var,
    user_id_var,
    add_global_fields,
    add_context_vars,
    IndentationProcessor,
    FunctionNameProcessor,
    # TruncationProcessor,  # Uncomment if needed
    # AlignmentProcessor     # Uncomment if needed
)
from structlog.stdlib import ProcessorFormatter

# from . import use_structured_log_indent  # Import function to switch log_indent decorator
from .log_indent_switcher import use_structured_log_indent


def set_request_context(request_id, user_id):
    request_id_var.set(request_id)
    user_id_var.set(user_id)

def setup_structured_logging(level=logging.INFO, truncate_messages=False, indent_spaces=4):
    """
    Configure structured logging using structlog with JSON output, indentation, and contextvars.
    This function sets up logging so that all logs are structured and includes request_id, user_id,
    indentation levels, and function names.
    """

  

    processors = [
        add_global_fields,    # Add global fields (app_version, env)
        add_context_vars,     # Add request_id, user_id from contextvars
        structlog.processors.TimeStamper(fmt="ISO", utc=True),
        FunctionNameProcessor(),
        IndentationProcessor(indent_spaces=indent_spaces),
        # Add truncation or alignment if needed:
        # TruncationProcessor(max_length=100),
        # AlignmentProcessor(start_column=60),

        # wrap_for_formatter is necessary so that ProcessorFormatter can handle the event
        structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
    ]




    structlog.configure(
        processors=processors,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        wrapper_class=structlog.stdlib.BoundLogger,
        cache_logger_on_first_use=True,
    )

    

    # ProcessorFormatter will apply JSONRenderer as the final step
    formatter = ProcessorFormatter(
        processor=structlog.processors.JSONRenderer(sort_keys=True),
        foreign_pre_chain=[],
    )

    

    handler = logging.StreamHandler(sys.stdout)
    handler.setFormatter(formatter)

    root_logger = logging.getLogger()

    
    root_logger.handlers = [handler]
    root_logger.setLevel(level)

    


    # Switch global log_indent to the structured one
    use_structured_log_indent()
