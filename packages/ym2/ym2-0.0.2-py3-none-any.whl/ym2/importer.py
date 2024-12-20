from pathlib import Path
from importlib import import_module
import sys

class ClassImporter:
    def __init__(self, path: str):
        self.path = path

    def import_class(self):
        cwd = str(Path.cwd())
        if cwd not in sys.path:
            sys.path.append(cwd)

        modules = self.path.split('.')
        imported = import_module(modules[0])

        for idx in range(1, len(modules)):
            try:
                imported = getattr(imported, modules[idx])
            except AttributeError:
                sub_module = '.'.join(modules[:idx + 1])
                imported = import_module(sub_module)
        return imported
