return {
  'hrsh7th/nvim-cmp',
  dependencies = {
    'hrsh7th/cmp-nvim-lsp',
    -- 'VonHeikemen/lsp-zero.nvim',
  },
  config = function()
    local cmp = require('cmp')
    -- local lsp_zero = require('lsp-zero')
    -- local cmp_action = lsp_zero.cmp_action()

    cmp.setup({
      sources = {
        {name = 'nvim_lsp'},
      },
      mapping = cmp.mapping.preset.insert({
        -- <C-m> is interpreted as <C-CR>
        ['<C-Enter>'] = cmp.mapping.confirm({
            behavior = cmp.ConfirmBehavior.Replace,
            select = true
        }),
        -- <C-m> is interpreted as <C-CR>
        -- ['<C-m>'] = cmp.mapping.complete(),
        ['<C-j>'] = cmp.mapping.select_next_item(),
        ['<C-k>'] = cmp.mapping.select_prev_item(),
        ['<C-h>'] = cmp.mapping.scroll_docs(-4),
        ['<C-l>'] = cmp.mapping.scroll_docs(4),
      }),
      snippet = {
        expand = function(args)
          vim.snippet.expand(args.body)
        end,
      },
    })
  end,
}
