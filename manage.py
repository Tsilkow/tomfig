from dataclasses import dataclass
from typing import List
import os
import os.path as osp
import shutil

import click
import git

from metaconfig import configs as raw_configs, config_sets as raw_config_sets


@dataclass
class Config(object):
    name: str
    filepaths: List[str]
    target_directory: str

    def __repr__(self):
        return f'{self.name}, {self.filepaths} -> {self.target_directory}'


def read_metaconfig(verbose: bool=False):
    configs = {}
    config_sets = {}

    for name, config in raw_configs.items():
        if name in configs:
            print(f'Config of name {name} has already been created. Discarding duplicate ...')
            continue
        configs[name] = Config(name=name, filepaths=config['filepaths'], target_directory=config['target_directory'])
        config_sets[f'{name}_only'] = [configs[name]]

    for name, config_names in raw_config_sets.items():
        if name in config_sets:
            print(f'Config set of name {name} has already been created. Discarding duplicate ...')
            continue
        config_sets[name] = [configs[c_name] for c_name in config_names]

    if verbose:
        print(f'Read metaconfig, found {len(configs)} configs and {len(config_sets)} config sets.')
	
    return config_sets


def move_file(source_dir, target_dir, filepath):
    source = osp.join(source_dir, filepath)
    target = osp.join(target_dir, filepath)
    try:
        shutil.copyfile(source, target)
    except OSError as error:
        print(f'\nMoving config file `{filepath}` from `{source}` to `{target}` failed due to following error: \n{error}\nAborting ...')
        return False
    return True


def move_directory(source_dir, target_dir, dirpath):
    source = osp.join(source_dir, dirpath)
    target = osp.join(target_dir, dirpath)
    try:
        shutil.copytree(source, target, dirs_exist_ok=True)
    except OSError as error:
        print(f'\nMoving config files `{dirpath}*` from `{source}` to `{target}` failed due to following error: \n{error}\nAborting ...')
        return False
    return True


def move_thing(source_dir, target_dir, thingpath, create_dir_if_not_exist: bool=True):
    if create_dir_if_not_exist and not osp.isdir(target_dir):
        os.makedirs(target_dir)
    if thingpath == '*':
        return move_directory(source_dir, target_dir, '')
    elif thingpath[-1] == '/': 
        return move_directory(source_dir, target_dir, thingpath)
    else:
        return move_file(source_dir, target_dir, thingpath)


def get_config_dir(tomfig_dir: str, config: Config):
    return osp.join(tomfig_dir, 'configs', config.name)
	

def move_configs_from_target(tomfig_dir: str, configs: List[Config]):
    for config in configs:
        config_dir = get_config_dir(tomfig_dir, config)
        for filepath in config.filepaths:
            status = move_thing(config.target_directory, config_dir, filepath)
            if not status: return False
    return True


def move_configs_to_target(tomfig_dir: str, configs: List[Config]):
    for config in configs:
        config_dir = get_config_dir(tomfig_dir, config)
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
            if confirmation in list('YyNn'): break
        if confirmation in list('Yy'): break

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
    config_sets = read_metaconfig(verbose)
    if config_set not in config_sets: 
        print(f'Selected config set {config_set} was not found in metaconfig. Aborting ...')
        return False
    configs = config_sets[config_set]
    if verbose:
        print(f'Tomfig directory: {tomfig_dir}')
        print(f'Config set: {config_set}')
        for config in configs:
            print(config)

    # with git.Repo(tomfig_dir) as repo:
    #     if repo.bare:
    #         print(f'No repository found at {tomfig_dir}. Aborting ...')
    #         return False
    # 	
    #     origin = repo.remotes.origin
    #     origin.pull()

    if verbose: print(f'\rPulling configs to local directories ...', end='', flush=True)
    if not move_configs_to_target(tomfig_dir, configs): return False
    if verbose: print(f'\rPulling configs to local directories [DONE]', flush=True)

    if verbose: print(f'Config update completed successfully!')
    return True


@cli.command()
@click.argument('config_set', type=str)
@click.option('--tomfig_dir', default=DEFAULT_TOMFIG_DIR, show_default=True, type=click.Path(exists=True))
@click.option('--verbose/--silent', default=True)
def push(config_set: str, tomfig_dir: str, verbose: bool=True):
    config_sets = read_metaconfig(verbose)
    if config_set not in config_sets: 
        print(f'Selected config set {config_set} was not found in metaconfig. Aborting ...')
        return False
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

    if verbose: print(f'\rPushing configs from local directories ...', end='', flush=True)
    if not move_configs_from_target(tomfig_dir, configs): return False
    if verbose: print(f'\rPushing configs from local directories [DONE]', flush=True)

    with git.Repo(tomfig_dir) as repo:
        # Commented out to allow better control over pushed files
        # commit_message = get_commit_message(repo)
        repo.git.add(update=True)
        # repo.index.commit(commit_message)
        # origin.push()

    if verbose: print(f'Configs are ready to be pushed!')
    return True


if __name__ == '__main__':
    cli()
