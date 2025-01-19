return {
  {
    'nvimtools/none-ls.nvim',
    enabled = false,
    config = function()
      local null_ls = require('null-ls')
      null_ls.setup({
        debug=true,
        sources = {
          null_ls.builtins.formatting.black,
          null_ls.builtins.diagnostics.flake8,
          null_ls.builtins.formatting.stylua,
        }
      })
      vim.keymap.set({'n', 'v'}, '<leader>f', function() vim.lsp.buf.format() end, opts)
    end
  }
}
