from pathlib import Path
from omegaconf import OmegaConf
from importlib import import_module
from typing import Any
import sys

def import_class(path: str):
    cwd = str(Path.cwd())
    if cwd not in sys.path:
        sys.path.append(cwd)

    modules = path.split('.')
    imported = import_module(modules[0])

    for idx in range(1, len(modules)):
        try:
            imported = getattr(imported, modules[idx])
        except AttributeError:
            sub_module = '.'.join(modules[:idx + 1])
            imported = import_module(sub_module)
    return imported
