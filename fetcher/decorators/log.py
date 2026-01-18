import logging

def log(func):
    def wrapper(*args, **kwargs):
        try:
            logging.info(f"Calling {func.__name__} with args {args} and kwargs {kwargs}")
        except Exception as e:
            logging.error(f"Error calling {func.__name__}: {e}")
        return func(*args, **kwargs)
    return wrapper
