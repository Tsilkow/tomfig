import os
import os.path as osp


HOME = os.getenv("HOME")


configs = {
    'kanata': {
        'filepaths': ['*'],
        'target_directory': osp.join(HOME, '.config/kanata/'),
    },
    'vim': {
        'filepaths': ['.vimrc'],
        'target_directory': HOME,
    },
    'bash_aliases': {
        'filepaths': ['.bash_aliases'],
        'target_directory': HOME,
    },
    'ideavim': {
        'filepaths': ['.ideavimrc'],
        'target_directory': HOME,
    },
    'tmux_home': {
        'filepaths': ['.tmux.conf'],
        'target_directory': HOME,
    },
    'tmux_remote': {
        'filepaths': ['.tmux.conf'],
        'target_directory': HOME,
    },
    'neovim': {
        'filepaths': ['init.lua', 'lua/core/', 'lua/plugins/'],
        'target_directory': osp.join(HOME, '.config/nvim/'),
    },
    'test1': {
        'filepaths': ['file1'],
        'target_directory': osp.join(HOME, 'tomfig/tests/test1/'),
    },
    'test2': {
        'filepaths': ['file2', 'dir1/'],
        'target_directory': osp.join(HOME, 'tomfig/tests/test2/'),
    },
    'test3': {
        'filepaths': ['*'],
        'target_directory': osp.join(HOME, 'tomfig/tests/test3/'),
    },
}

config_sets = {
    'remote': ['bash_aliases', 'vim', 'tmux_remote'],
    'home': ['kanata', 'vim', 'bash_aliases', 'ideavim', 'tmux_home', 'neovim'],
    'test': ['test1', 'test2', 'test3'],
}

