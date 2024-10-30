from collections import Counter
from shutil import copy, copytree
from enum import Enum
import os
import os.path as osp
import sys
from typing import Dict, List, Tuple
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
    return check_symlinks(tomfig_root, raw_configs, True)[0]


def create_symlink(tomfig_root: str, config_name: str, config_path: str):
    tomfig_dir = osp.join(tomfig_root, 'configs', config_name)
    os.makedirs(osp.dirname(config_path), exist_ok=True)
    os.symlink(tomfig_dir, config_path)


def handle_not_link(tomfig_root: str, config_name: str, config_path: str, do_backups: bool):
    if do_backups:
        backup_path = osp.join(osp.dirname(config_path), osp.basename(config_path)+'.bckp')
        if osp.isfile(config_path):
            copy(config_path, backup_path)
        elif osp.isdir(config_path):
            copytree(config_path, backup_path)
        else:
            raise Exception('Neither a file nor a directory')
    os.remove(config_path)
    create_symlink(tomfig_root, config_name, config_path)


def handle_incorrect(tomfig_root: str, config_name: str, config_path: str, overwrite_links: bool):
    if not overwrite_links: return False
    os.remove(config_path)
    create_symlink(tomfig_root, config_name, config_path)


def setup(
        tomfig_root: str, 
        config_set: Dict[str, str], 
        do_backups: bool, 
        overwrite_links: bool, 
        verbose: bool=True
):
    is_all_correct, report = check_symlinks(tomfig_root, config_set, verbose)
    if is_all_correct: return True
	
    for config_name, status in report.items():
        config_path = config_set[config_name]
        match status:
            case Status.REPO_MISSING:
                continue
            case Status.LOCAL_MISSING:
                create_symlink(tomfig_root, config_name, config_path)
            case Status.NOT_LINK:
                handle_not_link(tomfig_root, config_name, config_path, do_backups)
            case Status.INCORRECT:
                handle_incorrect(tomfig_root, config_name, config_path, overwrite_links)
            case Status.CORRECT:
                continue

    return check_symlinks(tomfig_root, config_set, verbose)[0]


def add_config(tomfig_root: str, config_name: str, config_path: str, create_backup: bool):
    tomfig_dir = osp.join(tomfig_root, 'configs', config_name)


def test_no_local():
    config = {'test': raw_configs['test']} 
    is_all_correct, report = \
    	check_symlinks(DEFAULT_TOMFIG_ROOT, config, False)
    assert(not is_all_correct)
    assert(report['test'] == Status.LOCAL_MISSING)

    assert(setup(DEFAULT_TOMFIG_ROOT, config, False, False, False))
    assert(check_symlinks(DEFAULT_TOMFIG_ROOT, config, False)[0])

    os.remove(raw_configs['test'])
    return True


def test_not_link():
    config = {'test': raw_configs['test']} 
    test_content = "Whispers of the breeze,\n" \
                   "Cherry blossoms kiss the sky,\n" \
                   "Spring’s sweet breath awakens.\n"
    with open(raw_configs['test'], 'w') as file:
        file.write(test_content)

    is_all_correct, report = check_symlinks(DEFAULT_TOMFIG_ROOT, config, False)
    assert(not is_all_correct)
    assert(report['test'] == Status.NOT_LINK)

    assert(setup(DEFAULT_TOMFIG_ROOT, config, True, False, False))
    assert(check_symlinks(DEFAULT_TOMFIG_ROOT, config, False)[0])
    backup_path = raw_configs['test']+'.bckp'
    with open(backup_path, 'r') as file:
        backup_content = file.read()
    assert(test_content == backup_content)

    os.remove(raw_configs['test'])
    os.remove(backup_path)
    return True


def test_incorrect():
    config = {'test': raw_configs['test']} 
    os.symlink(DEFAULT_TOMFIG_ROOT, osp.join(DEFAULT_TOMFIG_ROOT, 'test'))

    is_all_correct, report = \
    	check_symlinks(DEFAULT_TOMFIG_ROOT, {'test': raw_configs['test']}, False)
    assert(not is_all_correct)
    assert(report['test'] == Status.INCORRECT)

    assert(setup(DEFAULT_TOMFIG_ROOT, config, False, True, False))
    assert(check_symlinks(DEFAULT_TOMFIG_ROOT, config, False)[0])

    os.remove(raw_configs['test'])
    return True


def test_correct():
    config = {'test': raw_configs['test']} 
    create_symlink(DEFAULT_TOMFIG_ROOT, 'test', config['test'])

    is_all_correct, report = \
    	check_symlinks(DEFAULT_TOMFIG_ROOT, config, False)
    assert(is_all_correct)
    assert(report['test'] == Status.CORRECT)

    os.remove(config['test'])
    return True

def test(verbose: bool=False):
    if verbose: print('Testing ...', end='')
    test_no_local()
    test_not_link()
    test_incorrect()
    test_correct()
    if verbose: print('\rTests successfully completed')
    

if __name__ == '__main__':
    test(True)
    # full_check()
	
