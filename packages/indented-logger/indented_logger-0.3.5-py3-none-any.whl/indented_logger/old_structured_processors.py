# indented_logger/structured_processors.py
import contextvars
import inspect


# print("[DEBUG] structured_processors module loaded from:", __file__)

indent_level = contextvars.ContextVar("indent_level", default=0)

request_id_var = contextvars.ContextVar("request_id", default=None)
user_id_var = contextvars.ContextVar("user_id", default=None)


def add_context_vars(logger, method_name, event_dict):

    # print("[DEBUG add_context_vars] Start with:", event_dict)

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
    Decorator to increase indent before function call and decrease after.
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
        # Prepend indentation spaces to event text
        event = (" " * (lvl * self.indent_spaces)) + event
        event_dict["event"] = event
       
        return event_dict

class FunctionNameProcessor:
    def __call__(self, logger, method_name, event_dict):
       
        stack = inspect.stack()
        func_name = "<unknown>"
        for frame_info in stack:
            module_name = frame_info.frame.f_globals["__name__"]
            # Exclude frames from structlog and your own processor module
            if "structlog" not in module_name and "processors" not in module_name:
                func_name = frame_info.function
                break
        event_dict["func_name"] = func_name
      
        return event_dict

# class FunctionNameProcessor:
#     """
#     A structlog processor to extract the calling function's name.
#     It uses stack inspection to find the appropriate caller frame.
#     """
#     def __call__(self, logger, method_name, event_dict):
#         # We go up the stack frames to find the caller
#         # Adjust the index as needed depending on your code structure.
#         # Here, we try a few frames up until we find a suitable caller frame.
#         stack = inspect.stack()
#         # stack[0] = current, stack[1] = __call__ of processor, stack[2+] = caller
#         # We'll pick stack[3] or further to skip internal structlog frames.
#         if len(stack) > 3:
#             caller_frame = stack[3]
#             func_name = caller_frame.function
#         else:
#             func_name = "<unknown>"
#         event_dict["func_name"] = func_name
#         return event_dict


class TruncationProcessor:
    """
    A structlog processor to truncate the event message if it's too long.
    """
    def __init__(self, max_length=50):
        self.max_length = max_length

    def __call__(self, logger, method_name, event_dict):
        event = event_dict.get("event", "")
        if len(event) > self.max_length:
            event = event[:self.max_length - 3] + "..."
        event_dict["event"] = event
        return event_dict



class AlignmentProcessor:
    """
    A structlog processor to align the event message at a given column.
    This pads the message with spaces so that it effectively "starts" at a certain column.
    """
    def __init__(self, start_column=60):
        self.start_column = start_column

    def __call__(self, logger, method_name, event_dict):
        event = event_dict.get("event", "")
        stripped_event = event.lstrip()
        current_length = len(stripped_event)
        if current_length < self.start_column:
            padding = " " * (self.start_column - current_length)
            aligned_event = padding + stripped_event
        else:
            aligned_event = stripped_event
        event_dict["event"] = aligned_event
        return event_dict
