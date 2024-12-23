from typing import Union
from functools import wraps
from http import HTTPStatus

def HttpCode(status_code: Union[int, HTTPStatus]):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        # Convertir HTTPStatus a int si es necesario
        code = status_code.value if isinstance(status_code, HTTPStatus) else status_code
        setattr(wrapper, "__http_code__", code)
        return wrapper
    return decorator 