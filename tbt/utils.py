import re
import time
from functools import wraps
import logging
from typing import Any, Callable


def camel_to_snake(name: str) -> str:
    """
    Convert CamelCase to snake_case
    """
    name = re.sub('(.)([A-Z][a-z]+)', r'\1_\2', name)
    return re.sub('([a-z0-9])([A-Z])', r'\1_\2', name).lower()


def log_details(func) -> Callable:
    """Decorator to log function duration and arguments"""
    @wraps(func)
    def wrapper(*args, **kwargs) -> Any:
        kwargs_output = ", ".join([f"{k}={v}" for k, v in kwargs.items()])
        logging.info(f"Running {func.__name__}, with: {kwargs_output}")
        start_time = time.perf_counter()
        result = func(*args, **kwargs)
        end_time = time.perf_counter()
        total_time = end_time - start_time
        logging.info(f"{func.__name__} duration: {total_time:.4f}s")
        return result
    return wrapper
