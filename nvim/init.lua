-- Source file with vimrc setup
nvimrc='~/.config/nvim/'
vim.cmd('source ' .. nvimrc .. 'vimrc.vim')

-- Setup lazy.nvim
local lazypath = vim.fn.stdpath('data') .. '/lazy/lazy.nvim'

-- Auto-install lazy.nvim if not present
if not vim.uv.fs_stat(lazypath) then
  print('Installing lazy.nvim....')
  vim.fn.system({
    'git',
    'clone',
    '--filter=blob:none',
    'https://github.com/folke/lazy.nvim.git',
    '--branch=stable', -- latest stable release
    lazypath,
  })
  print('Done.')
end

vim.opt.rtp:prepend(lazypath)

-- Install all plugins
require('lazy').setup({
  {'folke/tokyonight.nvim'},
})

-- Set theme
vim.opt.termguicolors = true
vim.cmd.colorscheme('tokyonight')
