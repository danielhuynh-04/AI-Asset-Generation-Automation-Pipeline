"""
retry_wrapper.py — Exponential backoff retry decorator
Áp dụng tư duy error control từ ML pipeline: kiểm soát failure tại từng bước.
"""
import time
import logging
import functools
from typing import Callable, Any


logger = logging.getLogger(__name__)


def retry(max_attempts: int = 3, backoff_seconds: list[float] = None, exceptions: tuple = (Exception,)):
    """
    Decorator retry với exponential backoff.
    
    Args:
        max_attempts: số lần thử tối đa (default: 3)
        backoff_seconds: thời gian chờ giữa các lần thử [2, 4, 8] (default)
        exceptions: các exception cần retry (default: tất cả)
    
    Usage:
        @retry(max_attempts=3, backoff_seconds=[2, 4, 8])
        def call_api():
            ...
    """
    if backoff_seconds is None:
        backoff_seconds = [2.0, 4.0, 8.0]

    def decorator(func: Callable) -> Callable:
        @functools.wraps(func)
        def wrapper(*args, **kwargs) -> Any:
            last_exception = None
            for attempt in range(1, max_attempts + 1):
                try:
                    result = func(*args, **kwargs)
                    if attempt > 1:
                        logger.info(f"[RETRY] {func.__name__} succeeded on attempt {attempt}")
                    return result
                except exceptions as e:
                    last_exception = e
                    retry_count = attempt  # noqa — exposed for caller via exception
                    if attempt < max_attempts:
                        wait = backoff_seconds[min(attempt - 1, len(backoff_seconds) - 1)]
                        logger.warning(
                            f"[RETRY] {func.__name__} attempt {attempt}/{max_attempts} failed: {e}. "
                            f"Retrying in {wait}s..."
                        )
                        time.sleep(wait)
                    else:
                        logger.error(
                            f"[RETRY] {func.__name__} EXHAUSTED after {max_attempts} attempts. "
                            f"Last error: {e}"
                        )
            # Attach retry count to exception cho caller biết
            if last_exception:
                last_exception.retry_count = max_attempts  # type: ignore
            raise last_exception
        return wrapper
    return decorator


class RetryExhausted(Exception):
    """Raised khi đã dùng hết số lần retry."""
    def __init__(self, message: str, attempts: int, original_error: Exception):
        super().__init__(message)
        self.attempts = attempts
        self.original_error = original_error
