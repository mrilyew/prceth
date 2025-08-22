import importlib, pkgutil, os

__all__ = []

for _, module_name, is_pkg in pkgutil.iter_modules(importlib.import_module("declarable.Arguments").__path__):
    if not is_pkg:
        _imported = importlib.import_module("declarable.Arguments." + module_name)
        __all__.append(getattr(_imported, module_name))
        globals()[module_name] = getattr(_imported, module_name)
