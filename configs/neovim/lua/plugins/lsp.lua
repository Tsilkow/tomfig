return {
    {
        'williamboman/mason.nvim',
        config = function()
            require('mason').setup({})
        end
    },
    {
        'williamboman/mason-lspconfig.nvim',
        config = function()
            require('mason-lspconfig').setup({
                ensure_installed = {'lua_ls', 'pyright'}
            })
        end
    },
    {
        'neovim/nvim-lspconfig',
        config = function()
            local lspconfig = require('lspconfig')
        	lspconfig.lua_ls.setup({})
            lspconfig.pyright.setup({})

            vim.keymap.set('n', ',', '<cmd>lua vim.lsp.buf.hover()<cr>', opts)
            vim.keymap.set('n', 'gd', '<cmd>lua vim.lsp.buf.definition()<cr>', opts)
            vim.keymap.set('n', 'gD', '<cmd>lua vim.lsp.buf.declaration()<cr>', opts)
            vim.keymap.set('n', 'gi', '<cmd>lua vim.lsp.buf.implementation()<cr>', opts)
            vim.keymap.set('n', 'go', '<cmd>lua vim.lsp.buf.type_definition()<cr>', opts)
            vim.keymap.set('n', 'gr', '<cmd>lua vim.lsp.buf.references()<cr>', opts)
            vim.keymap.set('n', 'gs', '<cmd>lua vim.lsp.buf.signature_help()<cr>', opts)
            vim.keymap.set('n', '<leader>r', '<cmd>lua vim.lsp.buf.rename()<cr>', opts)
            vim.keymap.set('n', '<leader>e', '<cmd>lua vim.diagnostic.open_float()<cr>', opts)
            -- vim.keymap.set({'n', 'x'}, '<leader><Tab>', '<cmd>lua vim.lsp.buf.format({async = true})<cr>', opts)
            vim.keymap.set('n', '<leader> ', '<cmd>lua vim.lsp.buf.code_action()<cr>', opts)
        end
    }
}
--         'VonHeikemen/lsp-zero.nvim',
--   branch = 'v4.x',
--   config = function()
--     local lsp_zero = require('lsp-zero')
--
--     local lsp_attach = function(client, bufnr)
--       local opts = {buffer = bufnr}
--
--     end
--
--     lsp_zero.extend_lspconfig({
--       sign_text = true,
--       lsp_attach = lsp_attach,
--       capabilities = require('cmp_nvim_lsp').default_capabilities(),
--     })
--   end,
--   dependencies = {
--     {'neovim/nvim-lspconfig'},
--     {'hrsh7th/cmp-nvim-lsp'},
--   },
-- }
