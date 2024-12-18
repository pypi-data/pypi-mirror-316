from typing import Union, Dict, Any, Callable, Tuple
from importlib import import_module
from omegaconf import DictConfig, OmegaConf
from types import ModuleType


def create_component(
    comp: Callable[..., Any],
    args: Tuple[Any, ...],
    kwargs: Dict[str, Any],
) -> Any:
    return comp(*args, **kwargs)


def has_component(node: Union[Dict[str, Any], DictConfig]) -> bool:
    return OmegaConf.is_dict(node) or isinstance(node, dict) and '_component_' in node


def get_component_from_path(path: str) -> Any:
    if path == '':
        raise ValueError('empty path')
    parts = [part for part in path.split('.')]

    for part in parts:
        if not len(part):
            raise ValueError(
                f'Error loading `{path}`: invalid dot string.'
                '\nRelative imports are not supported.'
            )
    part0 = parts[0]
    try:
        obj = import_module(part0)
    except ImportError as exc_import:
        raise ValueError(
            f'Error loading `{path}`:\n{repr(exc_import)}'
            f'\nAre you sure that module `{part0}` is installed?'
        )

    for m in range(1, len(parts)):
        part = parts[m]
        try:
            obj = getattr(obj, part)
        # If getattr fails, check to see if it's a module we can import and
        # continue down the path
        except AttributeError as exc_attr:
            parent_dotpath = '.'.join(parts[:m])
            if isinstance(obj, ModuleType):
                mod = '.'.join(parts[: m + 1])
                try:
                    obj = import_module(mod)
                    continue
                except ModuleNotFoundError as exc_import:
                    raise ValueError(
                        f'Error loading `{path}`:\n{repr(exc_import)}'
                        f'Are you sure that `{part}` is importable from module `{parent_dotpath}`?'
                    ) from exc_import
                # Any other error trying to import module can be raised as
                # InstantiationError
                except Exception as exc_import:
                    raise ValueError(
                        f'Error loading `{path}`:\n{repr(exc_import)}'
                    ) from exc_import
            # If the component is not an attribute nor a module, it doesn't exist
            raise ValueError(
                f'Error loading `{path}`:\n{repr(exc_attr)}'
                f'Are you sure that `{part}` is an attribute of `{parent_dotpath}`?'
            ) from exc_attr

    return obj
