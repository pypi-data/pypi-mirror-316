from typing import Dict, Any
from omegaconf import DictConfig, OmegaConf
from ym2._component import has_component, get_component_from_path, create_component
import sys
import os


def instantiate_node(node: Dict[str, Any], *args: Any):
    if has_component(node):
        comp = get_component_from_path(node.get('_component_'))
        kwargs = {k: v for k, v in node.items() if k != '_component_'}
        return create_component(comp, args, kwargs)
    raise ValueError(
        'Cannot instantiate specified object.'
        "Make sure you've specified a _component_ field with a valid dotpath."
    )


def instantiate(config: DictConfig, *args: Any, **kwargs: Any) -> Any:
    if config is None:
        return None
    if not OmegaConf.is_dict(config):
        raise ValueError(f'instantiate only supports DictConfigs, got {type(config)}')
    if os.getcwd() not in sys.path:
        sys.path.append(os.getcwd())

    if kwargs:
        config = OmegaConf.merge(config, kwargs)

    OmegaConf.resolve(config)
    return instantiate_node(OmegaConf.to_object(config), *args)
