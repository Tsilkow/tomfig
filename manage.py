from typing import List
import os
import os.path as osp
import shutil

import click
import git

from configs import Config, config_sets


def move_file(source_dir, target_dir, filepath):
    source = osp.join(source_dir, filepath)
    target = osp.join(target_dir, filepath)
    try:
        shutil.move(source, target)
    except OSError as error:
        print(f'\nMoving config file `{filepath}` from `{source}` to `{target}` failed due to following error: \n{error}\nAborting ...')
        return False
    return True


def move_directory(source_dir, target_dir, dirpath):
    source = osp.join(source_dir, dirpath)
    target = osp.join(target_dir, dirpath)
    try:
        shutil.copytree(source, target)
    except OSError as error:
        print(f'\nMoving config files `{dirpath}*` from `{source}` to `{target}` failed due to following error: \n{error}\nAborting ...')
        return False
    return True


def move_thing(source_dir, target_dir, thingpath):
    full_thingpath = osp.join(source_dir, thingpath)
    if thingpath[-1] == '/' and osp.isdir(full_thingpath): 
        return move_directory(source_dir, target_dir, thingpath)
    elif thingpath[-1] != '/' and osp.isfile(full_thingpath): 
        return move_directory(source_dir, target_dir, thingpath)
    else: 
        print(f'\nInvalid path: {full_thingpath}\nAborting ...')
        return False
	

def move_configs_from_target(config_dir: str, configs: List[Config]):
    for config in configs:
        for filepath in config.filepaths:
            status = move_thing(config.target_directory, config_dir, filepath)
            if not status: return False
    return True


def move_configs_to_target(config_dir: str, configs: List[Config]):
    for config in configs:
        for filepath in config.filepaths:
            status = move_thing(config_dir, config.target_directory, filepath)
            if not status: return False
    return True


def get_commit_message(repo):
    diff = repo.index.diff(None)
    changed_files = [item.a_path for item in diff]
    while True:
        print(*changed_files, sep='\n')
        print(f'{len(changed_files)} files have been changed. Provide commit message.')
        message = input('> ')
        print(f'Your commit message is: {message}. \nDo you want to proceed?')
        while True:
            confirmation = input('(Y/n)> ')
            if confirmation in 'YyNn'.split(): break
        if confirmation in 'Yy'.split(): break

    return message


@click.group()
def cli():
    pass


DEFAULT_TOMFIG_DIR = f'{os.getenv("HOME")}/tomfig/' 


@cli.command()
@click.argument('config_set', type=str)
@click.option('--tomfig_dir', default=DEFAULT_TOMFIG_DIR, show_default=True, type=click.Path(exists=True))
@click.option('--verbose/--silent', default=True)
def pull(config_set: str, tomfig_dir: str, verbose: bool=True):
    assert config_set in config_sets.keys()
    configs = config_sets[config_set]
    if verbose:
        print(f'Tomfig directory: {tomfig_dir}')
        print(f'Config set: {config_set}')
        for config in configs:
            print(config)

    with git.Repo(tomfig_dir) as repo:
        if repo.bare:
            print(f'No repository found at {tomfig_dir}. Aborting ...')
            return False
    	
        origin = repo.remotes.origin
        origin.pull()

    if verbose: print(f'\rPushing configs to local directories ...', end='', flush=True)
    if not move_configs_to_target(tomfig_dir, configs): return False
    if verbose: print(f'\rPushing configs to local directories [DONE]', flush=True)

    if verbose: print(f'Config update completed successfully!')
    return True


@cli.command()
@click.argument('config_set', type=str)
@click.option('--tomfig_dir', default=DEFAULT_TOMFIG_DIR, show_default=True, type=click.Path(exists=True))
@click.option('--verbose/--silent', default=True)
def push(config_set: str, tomfig_dir: str, verbose: bool=True):
    assert config_set in config_sets.keys()
    configs = config_sets[config_set]
    if verbose:
        print(f'Tomfig directory: {tomfig_dir}')
        print(f'Config set: {config_set}')
        for config in configs:
            print(config)

    with git.Repo(tomfig_dir) as repo:
        if repo.bare:
            print(f'No repository found at {tomfig_dir}. Aborting ...')
            return False

        origin = repo.remotes.origin
        origin.pull()

    if verbose: print(f'\rPulling configs from local directories ...', end='', flush=True)
    if not move_configs_from_target(tomfig_dir, configs): return False
    if verbose: print(f'\rPulling configs from local directories [DONE]', flush=True)

    with git.Repo(tomfig_dir) as repo:
        origin = repo.remotes.origin
        commit_message = get_commit_message(repo)
        repo.git.add(update=True)
        repo.git.commit(commit_message)
        origin.push()

    if verbose: print(f'Config push completed successfully!')
    return True


if __name__ == '__main__':
    cli()
