return {
  {
    'nvim-lua/plenary.nvim'
  },
  {
    'nvim-telescope/telescope.nvim',
    tag = '0.1.8',
    dependencies = { 'nvim-lua/plenary.nvim' },
    config = function()
      local telescope = require('telescope')
      local builtin = require('telescope.builtin')
      local actions = require("telescope.actions")

      vim.keymap.set('n', 'e', builtin.find_files,
        { desc = 'Telescope find files' })
      vim.keymap.set('n', '<leader>e', builtin.live_grep,
        { desc = 'Telescope live grep' })
      vim.keymap.set('n', 'b', builtin.buffers,
        { desc = 'Telescope buffers' })
      vim.keymap.set('n', '<leader>b', builtin.help_tags,
        { desc = 'Telescope help tags' })

      telescope.defaults = telescope.defaults or {}
      telescope.defaults.mappings = telescope.defaults.mappings or {}

      telescope.defaults.mappings.i = vim.tbl_extend("force", telescope.defaults.mappings.i or {}, {
        ["<C-j>"] = actions.move_selection_next,
        ["<C-k>"] = actions.move_selection_previous,
      })

      telescope.defaults.mappings.n = vim.tbl_extend("force", telescope.defaults.mappings.n or {}, {
        ["<C-j>"] = actions.move_selection_next,
        ["<C-k>"] = actions.move_selection_previous,
      })
    end
  },
  {
    'stevearc/dressing.nvim',
    opts = {},
  },
}
