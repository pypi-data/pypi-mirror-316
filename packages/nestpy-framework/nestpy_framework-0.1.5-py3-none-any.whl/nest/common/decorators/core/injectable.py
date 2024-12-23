from typing import Any, Type

def Injectable():
    def decorator(cls: Type[Any]) -> Type[Any]:
        setattr(cls, "__injectable__", True)
        return cls
    return decorator