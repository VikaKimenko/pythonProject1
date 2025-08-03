from functools import wraps
from pathlib import Path
from typing import Any, Callable, TypeVar, Union

T = TypeVar("T")


def log(filename: Union[str, Path, None] = None) -> Callable[[Callable[..., T]], Callable[..., T]]:
    def decorator(func: Callable[..., T]) -> Callable[..., T]:
        @wraps(func)
        def wrapper(*args: Any, **kwargs: Any) -> T:
            try:
                result = func(*args, **kwargs)
                log_message = f"{func.__name__} ok"
                return result
            except Exception as e:
                log_message = f"{func.__name__} error: {type(e).__name__}. Inputs: {args}, {kwargs}"
                raise
            finally:
                if filename:
                    with open(str(filename), "a", encoding="utf-8") as f:
                        f.write(log_message + "\n")
                else:
                    print(log_message)

        return wrapper

    return decorator
