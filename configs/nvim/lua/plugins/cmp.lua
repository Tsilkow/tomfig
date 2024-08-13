return {
  'hrsh7th/nvim-cmp',
  dependencies = {
    'hrsh7th/cmp-nvim-lsp',
  },
  config = function()
    local cmp = require('cmp')
    local lsp_zero = require('lsp-zero')
    local cmp_action = lsp_zero.cmp_action()

    cmp.setup({
      sources = {
        {name = 'nvim_lsp'},
      },
      mapping = cmp.mapping.preset.insert({
        ['<CR>'] = cmp.mapping.confirm({select = false}),
        ['<C-CR>'] = cmp.mapping.complete(),
        ['<C-f>'] = cmp_action.vim_snippet_jump_forward(),
        ['<C-b>'] = cmp_action.vim_snippet_jump_backward(),
        ['<C-u>'] = cmp.mapping.scroll_docs(-4),
        ['<C-d>'] = cmp.mapping.scroll_docs(4),
      }),
      snippet = {
        expand = function(args)
          vim.snippet.expand(args.body)
        end,
      },
    })
  end,
}
