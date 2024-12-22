# bamboo/utils.py
import logging
from functools import wraps
from bamboo.settings.log import is_logging_enabled

# Configure logging here, if not already done globally
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')

# Logging decorator
def log(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        if is_logging_enabled():
            logging.info(f"LOG: ({func.__module__}, {func.__name__}) entered.")
            try:
                result = func(*args, **kwargs)
                logging.info(f"LOG: ({func.__module__}, {func.__name__}) executed successfully.")
                return result
            except Exception as e:
                logging.error(f"LOG: ({func.__module__}, {func.__name__}) failed with {e}.")
                raise
        else:
            return func(*args, **kwargs)
    return wrapper
