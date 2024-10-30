import os
import os.path as osp


HOME = str(os.getenv("HOME"))


configs = {
    'kanata': osp.join(HOME, '.config/kanata/'),
    'kanata_systemd': osp.join(HOME, '.config/systemd/user/kanata.service'),
    'vim': osp.join(HOME, '.vimrc'),
    'kitty': osp.join(HOME, '.config/kitty'),
    'bash_config': osp.join(HOME, '.bash_config'),
    'ideavim': osp.join(HOME, '.ideavimrc'),
    'tmux': osp.join(HOME, '.tmux.conf'),
    'neovim': osp.join(HOME, '.config/nvim'),
    'test': osp.join(HOME, 'tomfig/test'),
}

config_sets = {
    'remote': ['bash_config', 'vim', 'tmux'],
    'home': ['kanata', 'kanata_systemd', 'vim', 'kitty', 'bash_config', 'ideavim', 'tmux', 'neovim'],
}
