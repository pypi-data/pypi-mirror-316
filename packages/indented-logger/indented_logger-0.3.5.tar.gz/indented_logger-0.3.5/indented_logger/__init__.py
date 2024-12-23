# this is indented_logger/__init__.py

from .log_indent_switcher import log_indent, use_structured_log_indent, use_normal_log_indent

from .logging_config import setup_logging
from .structured_logging_setup import setup_structured_logging, set_request_context
from .structured_processors import log_indent

from .indent import increase_indent, decrease_indent, get_indent_level
from .decorator import log_indent as normal_log_indent
from .smart_logger import smart_indent_log
from .formatter import IndentFormatter



__all__ = [
    "use_structured_log_indent",
    "use_normal_log_indent",
    "log_indent",
    "setup_logging",
    "setup_structured_logging",
    "set_request_context",
    "increase_indent",
    "decrease_indent",
    "get_indent_level",
    "IndentFormatter",
    "smart_indent_log",
]

