from collections import Counter
from enum import Enum
import os
import os.path as osp
import sys
from typing import Dict, List
from metaconfig import configs as raw_configs, config_sets as raw_config_sets


DEFAULT_TOMFIG_ROOT = f'{os.getenv("HOME")}/tomfig/' 


class Status(Enum):
    REPO_MISSING = 0
    LOCAL_MISSING = 1
    NOT_LINK = 2
    INCORRECT = 3
    CORRECT = 4


def check_symlinks(tomfig_root: str, config_set: Dict[str, str], verbose: bool=True):
    report = {}
    for config_name, config_location in config_set.items():
        tomfig_dir = osp.join(tomfig_root, 'configs', config_name)
        if not osp.exists(tomfig_dir):
            report[config_name] = Status.REPO_MISSING
            continue
        if not osp.exists(config_location): 
            report[config_name] = Status.LOCAL_MISSING
            continue
        if not osp.islink(config_location): 
            report[config_name] = Status.NOT_LINK
            continue
        linked_file = os.readlink(config_location)
        if not linked_file == tomfig_dir:
            report[config_name] = Status.INCORRECT
            continue
        report[config_name] = Status.CORRECT

    is_all_correct = all([x == Status.CORRECT for x in report.values()])
    status_counts = Counter(report.values())
    if verbose:
        print('---[ SYMLINK CHECK ]---\n')
        for config_name, status in report.items():
            print(f'{config_name}: {status.name}')
        print('')
        for status_key, status_count in status_counts.items():
            print(f'{status_key}: {status_count}')
        print('')
        if is_all_correct: print('All symlinks are correct.')
        else: print('Some symlinks are not setup up.')

    return is_all_correct, report


def full_check(tomfig_root: str=DEFAULT_TOMFIG_ROOT):
    check_symlinks(tomfig_root, raw_configs, True)


if __name__ == '__main__':
    full_check()
	
