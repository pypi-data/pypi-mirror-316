# this is log_indent_switcher.py

from .decorator import log_indent as normal_log_indent
from .structured_processors import log_indent as structured_log_indent

# The "active" log_indent
log_indent = normal_log_indent

def use_structured_log_indent():
    global log_indent
    log_indent = structured_log_indent

def use_normal_log_indent():
    global log_indent
    log_indent = normal_log_indent


# from .structured_processors import log_indent as structured_log_indent
# from .decorator import log_indent as normal_log_indent

# def use_structured_log_indent():
#     from indented_logger import log_indent
#     globals()['log_indent'] = structured_log_indent

# def use_normal_log_indent():
#     from indented_logger import log_indent
#     globals()['log_indent'] = normal_log_indent
