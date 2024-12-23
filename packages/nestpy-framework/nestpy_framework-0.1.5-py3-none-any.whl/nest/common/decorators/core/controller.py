from typing import Any, Type, Optional

def Controller(prefix: str = "", version: Optional[str] = None):
    def decorator(cls: Type[Any]) -> Type[Any]:
        setattr(cls, "__controller__", True)
        setattr(cls, "__prefix__", prefix)
        setattr(cls, "__version__", version)
        
        return cls
    return decorator