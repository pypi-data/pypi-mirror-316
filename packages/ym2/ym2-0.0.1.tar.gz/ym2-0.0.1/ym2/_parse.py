from typing import Tuple, List
from argparse import Namespace
from omegaconf import DictConfig, OmegaConf
from pathlib import Path
from ym2._sweeper import sweep
import argparse
import pydash
import yaml


def parse_unknown_args() -> Tuple[Namespace, List[str]]:
    parser = argparse.ArgumentParser()
    parser.add_argument('config_file', type=str)
    args, unknown_args = parser.parse_known_args()
    unknown_flag_args = [arg for arg in unknown_args if arg.startswith('--')]
    if unknown_flag_args:
        raise ValueError(f'Additional flag arguments not supported: {unknown_flag_args}. Please use key=value')
    return args, unknown_args


def merge_yaml_and_cli_args(yaml_args: Namespace, cli_args: List[str]) -> DictConfig:
    config_file = Path(yaml_args.config_file)
    assert config_file.exists(), f'Config file `{str(config_file)}` does not exists'

    yaml_kwargs = yaml.safe_load(config_file.open())
    cli_dotlist = []

    for arg in cli_args:
        # Using flag (~) to remove key from yaml conf
        if arg.startswith('~'):
            dotpath = arg[1:].split('=')[0]
            if '_component_' in dotpath:
                raise ValueError(f'Remove components from CLI is not supported: {dotpath}')
            assert pydash.objects.has(yaml_kwargs, dotpath), f'Could not find key `{dotpath}` in yaml config file'
            pydash.objects.unset(yaml_kwargs, dotpath)
            continue
        try:
            k, v = arg.split('=')
        except (KeyError, ValueError):
            raise ValueError('Command-line overrides must be in form of key=value') from None
        # Otherwise, keep as original
        cli_dotlist.append(f'{k}={v}')

    yaml_conf = OmegaConf.create(yaml_kwargs)
    cli_conf = OmegaConf.from_dotlist(cli_dotlist)
    return OmegaConf.merge(yaml_conf, cli_conf)


def parse():
    yaml_args, cli_args = parse_unknown_args()
    conf = merge_yaml_and_cli_args(yaml_args, cli_args)
    sweep(conf)
