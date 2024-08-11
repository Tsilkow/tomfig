-- Source file with vimrc setup
nvimrc='~/.config/nvim/'
vim.cmd('source ' .. nvimrc .. 'vimrc.vim')

-- Setup lazy.nvim
local lazypath = vim.fn.stdpath('data') .. '/lazy/lazy.nvim'

-- Auto-install lazy.nvim if not present
if not vim.uv.fs_stat(lazypath) then
  print('installing lazy.nvim....')
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
  {'Mofiqul/dracula.nvim'},
  {'miikanissi/modus-themes.nvim'},
  {'bluz71/vim-moonfly-colors'},
  {'tiagovla/tokyodark.nvim'},
  {'rebelot/kanagawa.nvim'},
  {'rose-pine/neovim', as = 'rose-pine' },
  {'nvim-treesitter/nvim-treesitter',
    build = ':TSUpdate',
    config = function ()
      local configs = require("nvim-treesitter.configs")

      configs.setup({
          ensure_installed = { "c", "lua", "vim", "vimdoc", "query", "python", "html" },
          sync_install = false,
          highlight = { enable = true },
          indent = { enable = true },  
        })
    end
  },
  {'vonheikemen/lsp-zero.nvim', branch = 'v4.x'},
  {'williamboman/mason.nvim'},
  {'williamboman/mason-lspconfig.nvim'},
  {'neovim/nvim-lspconfig'},
  {'hrsh7th/cmp-nvim-lsp'},
  {'hrsh7th/nvim-cmp'},
  {
      'numtostr/comment.nvim',
      opts = {
        toggler = {
            line = "'",
        },
        opleader = {
            block = "'",
        },
      }
  }
})

-- LSP configufation
local lsp_zero = require('lsp-zero')

-- lsp_attach is where you enable features that only work
-- if there is a language server active in the file
local lsp_attach = function(client, bufnr)
  local opts = {buffer = bufnr}

  vim.keymap.set('n', ',', '<cmd>lua vim.lsp.buf.hover()<cr>', opts)
  vim.keymap.set('n', 'gd', '<cmd>lua vim.lsp.buf.definition()<cr>', opts)
  vim.keymap.set('n', 'gD', '<cmd>lua vim.lsp.buf.declaration()<cr>', opts)
  vim.keymap.set('n', 'gi', '<cmd>lua vim.lsp.buf.implementation()<cr>', opts)
  vim.keymap.set('n', 'go', '<cmd>lua vim.lsp.buf.type_definition()<cr>', opts)
  vim.keymap.set('n', 'gr', '<cmd>lua vim.lsp.buf.references()<cr>', opts)
  vim.keymap.set('n', 'gs', '<cmd>lua vim.lsp.buf.signature_help()<cr>', opts)
  vim.keymap.set('n', '<leader>r', '<cmd>lua vim.lsp.buf.rename()<cr>', opts)
  vim.keymap.set({'n', 'x'}, '<leader><Tab>', '<cmd>lua vim.lsp.buf.format({async = true})<cr>', opts)
  vim.keymap.set('n', '<leader>,', '<cmd>lua vim.lsp.buf.code_action()<cr>', opts)
end

lsp_zero.extend_lspconfig({
  sign_text = true,
  lsp_attach = lsp_attach,
  capabilities = require('cmp_nvim_lsp').default_capabilities(),
})

require('mason').setup({})
require('mason-lspconfig').setup({
  handlers = {
    function(server_name)
      require('lspconfig')[server_name].setup({})
    end,
  },
})

require('lspconfig').pyright.setup({})

-- Neovim-specific keybindings


-- Set theme
vim.opt.termguicolors = true
-- vim.cmd.colorscheme('tokyonight')
-- vim.cmd.colorscheme('dracula')
-- vim.cmd.colorscheme('modus')
-- vim.cmd.colorscheme('moonfly')
-- vim.cmd.colorscheme('tokyodark')
-- vim.cmd.colorscheme('kanagawa')
vim.cmd.colorscheme('rose-pine')
-- vim.api.nvim_set_hl(0, 'Normal', { bg = "none" })
-- vim.api.nvim_set_hl(0, 'NormalFloat', { bg = "none" })
