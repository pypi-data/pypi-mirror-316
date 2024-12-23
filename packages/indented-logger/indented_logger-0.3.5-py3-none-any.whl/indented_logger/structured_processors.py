import contextvars
import inspect

# Context variables
indent_level = contextvars.ContextVar("indent_level", default=0)
request_id_var = contextvars.ContextVar("request_id", default=None)
user_id_var = contextvars.ContextVar("user_id", default=None)

def add_context_vars(logger, method_name, event_dict):
    request_id = request_id_var.get()
    user_id = user_id_var.get()

    if request_id is not None:
        event_dict["request_id"] = request_id
    if user_id is not None:
        event_dict["user_id"] = user_id

    return event_dict

def add_global_fields(logger, method_name, event_dict):
    event_dict["app_version"] = "1.0.0"
    event_dict["env"] = "prod"
    return event_dict

def increase_indent():
    lvl = indent_level.get()
    indent_level.set(lvl + 1)

def decrease_indent():
    lvl = indent_level.get()
    indent_level.set(max(lvl - 1, 0))

def log_indent(func):
    """
    Decorator that increases indentation before the function call
    and decreases it after the function returns.
    """
    def wrapper(*args, **kwargs):
        increase_indent()
        try:
            return func(*args, **kwargs)
        finally:
            decrease_indent()
    return wrapper

class IndentationProcessor:
    """
    A structlog processor that applies indentation based on the current indentation level.
    """
    def __init__(self, indent_spaces=4):
        self.indent_spaces = indent_spaces

    def __call__(self, logger, method_name, event_dict):
        lvl = indent_level.get()
        event = event_dict.get("event", "")

        # Prepend indentation spaces based on indent_level
        indented_event = (" " * (lvl * self.indent_spaces)) + event
        event_dict["event"] = indented_event

        return event_dict

# class FunctionNameProcessor:
#     """
#     Extracts the calling function's name from the stack, skipping structlog frames.
#     """
#     def __call__(self, logger, method_name, event_dict):
#         stack = inspect.stack()
#         func_name = "<unknown>"
#         for frame_info in stack:
#             module_name = frame_info.frame.f_globals["__name__"]
#             if "structlog" not in module_name and "structured_processors" not in module_name:
#                 func_name = frame_info.function
#                 break
#         event_dict["func_name"] = func_name
#         return event_dict
    

class FunctionNameProcessor:
    def __call__(self, logger, method_name, event_dict):
        stack = inspect.stack()
        func_name = "<unknown>"
        for frame_info in stack:
            module_name = frame_info.frame.f_globals["__name__"]

            # Skip frames from structlog, your own processors, AND the stdlib logging module
            if (
                "structlog" in module_name
                or "structured_processors" in module_name
                or "logging" in module_name
            ):
                continue
            
            func_name = frame_info.function
            break

        event_dict["func_name"] = func_name
        return event_dict
