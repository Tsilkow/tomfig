from collections import Counter
from shutil import copy, copytree, rmtree
from enum import Enum
import os
import os.path as osp
from typing import Dict, Tuple

import click

from metaconfig import configs as raw_configs, config_sets as raw_config_sets


DEFAULT_TOMFIG_ROOT = osp.dirname(osp.realpath(__file__))


class Status(Enum):
    """
    Enum class for holding status of a given config.
    """
    REPO_MISSING = 0
    LOCAL_MISSING = 1
    NOT_LINK = 2
    INCORRECT = 3
    CORRECT = 4


def check_symlinks(
    tomfig_root: str, config_set: Dict[str, str], verbose: bool=True
) -> Tuple[bool, Dict[str, Status]]:
    """
    Looks through all configs in a given config sets and establishes their status.

    Arguments:
    tomfig_root(str): path to `tomfig/` directory.
    config_set(Dict[str, str]): dictionary of config name and its files.
    verbose(bool): flag for printing results.

    Returns:
    is_all_correct(bool): true if all configs are correct.
    report(Dict[str, Status]): statuses for all configs.

    """
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


def full_check(tomfig_root: str=DEFAULT_TOMFIG_ROOT) -> bool:
    """
    Helper function returning only whether all defined configs are correct.

    Arguments:
    tomfig_root(str): path to `tomfig/` directory.

    Returns:
    bool: true if all configs are correcly setup.
    """
    return check_symlinks(tomfig_root, raw_configs, True)[0]


def create_symlink(tomfig_root: str, config_name: str, config_path: str) -> None:
    """
    Creates symlink for a given config. Assumes the config is accessible.

    Arguments:
    tomfig_root(str): path to `tomfig/` directory.
    config_name(str): name of the config, used as directory name in `tomfig/configs/`.
    config_path(str): path to config file/directory that is to be symlinked.

    Returns:
    None
    """
    tomfig_dir = osp.join(tomfig_root, 'configs', config_name)
    print(config_path, osp.dirname(config_path))
    os.makedirs(osp.dirname(config_path), exist_ok=True)
    os.symlink(tomfig_dir, config_path)


def handle_not_link(tomfig_root: str, config_name: str, config_path: str, do_backups: bool) -> None:
    """
    Handles config entries that do exist, but are not symlinks. Assumes the config is accessible.

    Arguments:
    tomfig_root(str): path to `tomfig/` directory.
    config_name(str): name of the config, used as directory name in `tomfig/configs/`.
    config_path(str): path to config file/directory that is to be symlinked.
    do_backups(bool): if true, backup of config will be left at the original location.

    Returns:
    None
    """
    backup_path = osp.join(osp.dirname(config_path), osp.basename(config_path)+'.bckp')
    if osp.isfile(config_path):
        if do_backups:
            copy(config_path, backup_path)
        os.remove(config_path)
    elif osp.isdir(config_path):
        if do_backups:
            copytree(config_path, backup_path)
        rmtree(config_path)
    else:
        raise Exception('Neither a file nor a directory')
    create_symlink(tomfig_root, config_name, config_path)


def handle_incorrect(
    tomfig_root: str, config_name: str, config_path: str, overwrite_links: bool
) -> bool:
    """
    Handles config entries that are symlinks, but point incorrectly. Assumes the config is accessible.

    Arguments:
    tomfig_root(str): path to `tomfig/` directory.
    config_name(str): name of the config, used as directory name in `tomfig/configs/`.
    config_path(str): path to config file/directory that is to be symlinked.
    overwrite_links(bool): if true, incorrect links will be replaced.

    Returns:
    bool: true, if symlink was replaced.
    """
    if not overwrite_links: return False
    os.remove(config_path)
    create_symlink(tomfig_root, config_name, config_path)
    return True


def setup(
    tomfig_root: str, 
    config_set: Dict[str, str], 
    do_backups: bool, 
    overwrite_links: bool, 
    verbose: bool=True
) -> bool:
    """
    Sets up config symlinks based on assesment of current environment. 
    In case of config present in metaconfig, but absent in `configs/`,
    it does nothing.

    Arguments:
    tomfig_root(str): path to `tomfig/` directory.
    config_set(Dict[str, str]): dictionary of config name and its files.
    overwrite_links(bool): if true, incorrect links will be replaced.
    verbose(bool): flag for printing results.

    Returns:
    bool: true, if all symlinks (from given config set) are set up correctly.
    """
    is_all_correct, report = check_symlinks(tomfig_root, config_set, verbose)
    if is_all_correct: return True

    for config_name, status in report.items():
        config_path = config_set[config_name]
        if status == Status.REPO_MISSING:
            continue
        elif status == Status.LOCAL_MISSING:
            create_symlink(tomfig_root, config_name, config_path)
        elif status == Status.NOT_LINK:
            handle_not_link(tomfig_root, config_name, config_path, do_backups)
        elif status == Status.INCORRECT:
            handle_incorrect(tomfig_root, config_name, config_path, overwrite_links)
        elif status == Status.CORRECT:
            continue

    return check_symlinks(tomfig_root, config_set, verbose)[0]


def move_to_tomfig(
    tomfig_root: str, 
    config_name: str, 
    config_path: str, 
    do_backups: bool,
) -> bool:

    """
    Moves config from its local path to tomfig and creates symlink from 
    its orignal path. 

    Arguments:
    tomfig_root(str): path to `tomfig/` directory.
    config_name(str): name of the config, used as directory name in `tomfig/configs/`.
    config_path(str): path to config file/directory that is to be symlinked.
    do_backups(bool): if true, backup of config will be left at the original location.

    Returns:
    bool: true if config is successfully moved to tomfig. 
    """
    tomfig_path = osp.join(tomfig_root, 'configs', config_name)
    if osp.exists(tomfig_path):
        print(f'Config is already stored at path {tomfig_path}. Aborting ...')
        return False
    if not osp.exists(config_path):
        print(f'Given config path {config_path} is not accessible. Aborting ...')
        return False
    if osp.islink(config_path):
        print(f'Given config path {config_path} is a symlink. Aborting ...')
        return False

    if osp.isfile(config_path):
        copy(config_path, tomfig_path)
    elif osp.isdir(config_path):
        copytree(config_path, tomfig_path)
    else:
        raise Exception('Neither a file nor a directory')

    handle_not_link(tomfig_root, config_name, config_path, do_backups)

    return True


def test_no_local():
    config = {'test1': raw_configs['test1']} 
    is_all_correct, report = \
    check_symlinks(DEFAULT_TOMFIG_ROOT, config, False)
    assert(not is_all_correct)
    assert(report['test1'] == Status.LOCAL_MISSING)

    assert(setup(DEFAULT_TOMFIG_ROOT, config, False, False, False))
    assert(check_symlinks(DEFAULT_TOMFIG_ROOT, config, False)[0])

    os.remove(raw_configs['test1'])
    return True


def test_not_link():
    config = {'test1': raw_configs['test1']} 
    test_content = "Whispers of the breeze,\n" \
        "Cherry blossoms kiss the sky,\n" \
        "Spring’s sweet breath awakens.\n"
    with open(raw_configs['test1'], 'w') as file:
        file.write(test_content)

    is_all_correct, report = check_symlinks(DEFAULT_TOMFIG_ROOT, config, False)
    assert(not is_all_correct)
    assert(report['test1'] == Status.NOT_LINK)

    assert(setup(DEFAULT_TOMFIG_ROOT, config, True, False, False))
    assert(check_symlinks(DEFAULT_TOMFIG_ROOT, config, False)[0])
    backup_path = raw_configs['test1']+'.bckp'
    with open(backup_path, 'r') as file:
        backup_content = file.read()
    assert(test_content == backup_content)

    os.remove(raw_configs['test1'])
    os.remove(backup_path)
    return True


def test_incorrect():
    config = {'test1': raw_configs['test1']} 
    os.symlink(DEFAULT_TOMFIG_ROOT, raw_configs['test1'])

    is_all_correct, report = \
    check_symlinks(DEFAULT_TOMFIG_ROOT, {'test1': raw_configs['test1']}, False)
    assert(not is_all_correct)
    assert(report['test1'] == Status.INCORRECT)

    assert(setup(DEFAULT_TOMFIG_ROOT, config, False, True, False))
    assert(check_symlinks(DEFAULT_TOMFIG_ROOT, config, False)[0])

    os.remove(raw_configs['test1'])
    return True


def test_correct():
    config = {'test1': raw_configs['test1']} 
    create_symlink(DEFAULT_TOMFIG_ROOT, 'test1', config['test1'])

    is_all_correct, report = \
    check_symlinks(DEFAULT_TOMFIG_ROOT, config, False)
    assert(is_all_correct)
    assert(report['test1'] == Status.CORRECT)

    os.remove(config['test1'])
    return True


def test_move_to_tomfig():
    config = {'test2': raw_configs['test2']} 

    is_all_correct, report = \
    check_symlinks(DEFAULT_TOMFIG_ROOT, config, False)
    assert(not is_all_correct)
    assert(report['test2'] == Status.REPO_MISSING)

    move_to_tomfig(DEFAULT_TOMFIG_ROOT, 'test2', raw_configs['test2'], True)

    is_all_correct, report = \
    check_symlinks(DEFAULT_TOMFIG_ROOT, config, False)
    assert(is_all_correct)
    assert(report['test2'] == Status.CORRECT)

    os.remove(osp.join(DEFAULT_TOMFIG_ROOT, 'configs', 'test2'))
    os.rename(raw_configs['test2']+'.bckp', raw_configs['test2'])
    return True


def test(verbose: bool=False):
    if verbose: print('Testing ...', end='')
    test_no_local()
    test_not_link()
    test_incorrect()
    test_correct()
    test_move_to_tomfig()
    if verbose: print('\rTests successfully completed')


def read_metaconfig(verbose: bool=False) -> Dict[str, Dict[str, str]]:
    """
    Creates config sets described in metaconfig.

    Arguments:
    verbose(bool=True): flag for printing additional info.

    Returns:
    config_sets(Dict[str, str]): constructed config sets.
    """
    configs = {}
    config_sets = {}

    for name, config in raw_configs.items():
        if name in configs:
            print(f'Config of name {name} has already been created. Discarding duplicate ...')
            continue
        configs[name] = config.rstrip('/')
        config_sets[f'{name}_only'] = {name: configs[name]}

    for name, config_names in raw_config_sets.items():
        if name in config_sets:
            print(f'Config set of name {name} has already been created. Discarding duplicate ...')
            continue
        config_sets[name] = {c_name: configs[c_name] for c_name in config_names}

    if verbose:
        print(f'Read metaconfig, found {len(configs)} configs and {len(config_sets)} config sets.')

    return config_sets


@click.group()
def cli():
    pass


@cli.command()
@click.argument('config_set', type=str)
@click.option('--tomfig_root', default=DEFAULT_TOMFIG_ROOT, show_default=True, type=click.Path(exists=True))
@click.option('--verbose/--silent', default=True)
def check(config_set: str, tomfig_root: str, verbose: bool=True) -> None:
    config_sets = read_metaconfig(verbose=verbose)
    print(config_sets)
    check_symlinks(tomfig_root, config_sets[config_set], verbose=verbose)


@cli.command('setup')
@click.argument('config_set', type=str)
@click.option('--tomfig_root', default=DEFAULT_TOMFIG_ROOT, show_default=True, type=click.Path(exists=True))
@click.option('--backup', default=True, show_default=True, type=bool)
@click.option('--overwrite-links', default=True, show_default=True, type=bool)
@click.option('--verbose/--silent', default=True)
def setup_cli(
    config_set: str, 
    tomfig_root: str, 
    backup: bool, 
    overwrite_links: bool, 
    verbose: bool=True
) -> None:
    config_sets = read_metaconfig(verbose=verbose)
    setup(tomfig_root, config_sets[config_set], backup, overwrite_links, verbose)


@cli.command('move-to-tomfig')
@click.argument('config_set', type=str)
@click.option('--tomfig_root', default=DEFAULT_TOMFIG_ROOT, show_default=True, type=click.Path(exists=True))
@click.option('--backup', default=True, show_default=True, type=bool)
@click.option('--verbose/--silent', default=True)
def move_to_tomfig_cli(
    config_set: str, 
    tomfig_root: str, 
    backup: bool, 
    verbose: bool=True
) -> None:
    config_sets = read_metaconfig(verbose=verbose)
    selected_config = config_sets[config_set]
    for config_name, config_path in selected_config.items():
        if verbose: print(f'Moving {config_name} to tomfig (from {config_path}).')
        move_to_tomfig(tomfig_root, config_name, config_path, backup)


@cli.command('test')
def test_cli() -> None:
    test(True)


if __name__ == '__main__':
    cli()
