from dataclasses import dataclass
from typing import List


@dataclass
class Config(object):
    name: str
    filepaths: List[str]
    target_directory: str

    def __repr__(self):
        return f'{self.name}, {self.filepaths} -> {self.target_directory}'


vim_config = Config(
    name='vim', 
    filepaths=['.vimrc'],
    target_directory='~/'
)

tmux_config = Config(
    name='tmux', 
    filepaths=['.tmux.conf'],
    target_directory='~/'
)

neovim_config = Config(
    name='neovim', 
    filepaths=['init.lua', 'lua/core/', 'lua/plugins/'],
    target_directory='~/.config/nvim/'
)

test1_config = Config(
    name='test1',
    filepaths=['file1'],
    target_directory='~/tomfig/tests/test1/'
)

test2_config = Config(
    name='test2',
    filepaths=['file2', 'dir1/'],
    target_directory='~/tomfig/tests/test2/'
)

config_sets = {
    'minimal': [vim_config, tmux_config],
    'full': [vim_config, tmux_config, neovim_config],
    'test': [test1_config, test2_config],
}
