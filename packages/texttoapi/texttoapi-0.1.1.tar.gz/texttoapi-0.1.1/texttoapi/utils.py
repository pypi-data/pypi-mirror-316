import logging
import os
import inspect
from . import env

# Configure the logger
logging.getLogger(os.path.basename(__file__)).setLevel(logging.DEBUG if env.log_level == "debug" else logging.INFO)


def log_function_name():
    logging.getLogger(os.path.basename(__file__)).info(f"Calling function: {inspect.stack()[1][3]}")
