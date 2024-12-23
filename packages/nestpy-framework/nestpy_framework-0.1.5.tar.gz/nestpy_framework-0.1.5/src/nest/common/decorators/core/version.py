from functools import wraps

def Version(version: str):
    """
    Decorador para especificar la versión de la ruta.
    
    @Version("1")
    @Controller("/users")
    class UserController:
        pass
    """
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            return func(*args, **kwargs)
        
        setattr(wrapper, "__version__", version)
        return wrapper
    return decorator