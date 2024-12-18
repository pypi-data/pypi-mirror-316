from omegaconf import DictConfig, OmegaConf
from ym2._instantiate import instantiate
from typing import List
import multiprocessing
import itertools
import logging
import copy

logger = logging.getLogger(__name__)


def flatten_dict(conf: DictConfig, parent_key: str = '', sep: str = '.') -> List:
    items = []
    for k, v in conf.items():
        new_key = parent_key + sep + k if parent_key else k
        if isinstance(v, DictConfig):
            items += flatten_dict(v, new_key, sep=sep)
        else:
            items.append((new_key, v))
    return items


def process_task(conf: DictConfig) -> None:
    instantiate(conf)


def run_task_in_process(task_configs):
    logger.info(f'Launching {len(task_configs)} tasks locally.')
    for idx, task_config in enumerate(task_configs):
        logger.info(OmegaConf.to_yaml(task_config, resolve=True))
        process = multiprocessing.Process(target=process_task, args=(task_config,))
        process.start()
        process.join()
        logger.info(f'#{idx:02}: Process {process.pid} completed and cleaned up.')
    logger.info(f'Finished running {len(task_configs)} tasks locally.')


def sweep(conf: DictConfig):
    all_dotlist = []
    for flatten_key, val in flatten_dict(conf):
        if isinstance(val, str) and ',' in val:
            dotlist = []
            overrides = [override for override in val.split(',') if override]
            for override in overrides:
                dotlist.append(f'{flatten_key}={override}')
            all_dotlist.append(dotlist)
    combined_dotlist = list(itertools.product(*all_dotlist))

    task_configs = []
    for dotlist in combined_dotlist:
        copy_config = copy.deepcopy(conf)
        dot_config = OmegaConf.from_dotlist(dotlist)
        task_config = OmegaConf.merge(copy_config, dot_config)
        task_configs.append(task_config)

    run_task_in_process(task_configs)
