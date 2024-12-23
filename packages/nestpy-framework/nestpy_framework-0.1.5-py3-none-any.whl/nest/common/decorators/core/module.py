from dataclasses import dataclass
from typing import Any, Type, List, Optional

@dataclass
class ModuleMetadata:
    controllers: List[Type] = None
    providers: List[Type] = None
    imports: List[Type] = None
    exports: List[Type] = None

    def __post_init__(self):
        self.controllers = self.controllers or []
        self.providers = self.providers or []
        self.imports = self.imports or []
        self.exports = self.exports or []

def Module(
    *,
    controllers: List[Type] = None,
    providers: List[Type] = None,
    imports: List[Type] = None,
    exports: List[Type] = None
):

    def decorator(cls: Type[Any]) -> Type[Any]:
        metadata = ModuleMetadata(
            controllers=controllers,
            providers=providers,
            imports=imports,
            exports=exports
        )
        setattr(cls, "__module__", True)
        setattr(cls, "__metadata__", metadata)
        return cls

    return decorator