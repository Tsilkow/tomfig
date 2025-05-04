return {
	{
		"williamboman/mason.nvim",
		config = function()
			require("mason").setup({})
		end,
	},
	{
		"williamboman/mason-lspconfig.nvim",
		config = function()
			require("mason-lspconfig").setup({
				ensure_installed = { "lua_ls", "pyright", "gopls" },
			})
		end,
	},
	{
		"neovim/nvim-lspconfig",
		config = function()
			local lspconfig = require("lspconfig")
			lspconfig.gopls.setup({})
			lspconfig.lua_ls.setup({})
			lspconfig.pyright.setup({})

			vim.keymap.set("n", ",", "<cmd>lua vim.lsp.buf.hover()<cr>", opts)
			vim.keymap.set("n", "gd", "<cmd>lua vim.lsp.buf.definition()<cr>", opts)
			vim.keymap.set("n", "gD", "<cmd>lua vim.lsp.buf.declaration()<cr>", opts)
			vim.keymap.set("n", "gi", "<cmd>lua vim.lsp.buf.implementation()<cr>", opts)
			vim.keymap.set("n", "go", "<cmd>lua vim.lsp.buf.type_definition()<cr>", opts)
			vim.keymap.set("n", "gr", "<cmd>Telescope lsp_references<cr>", opts)
			vim.keymap.set("n", "gs", "<cmd>lua vim.lsp.buf.signature_help()<cr>", opts)
			vim.keymap.set("n", "<leader>r", "<cmd>lua vim.lsp.buf.rename()<cr>", opts)
			vim.keymap.set("n", "<leader>d", "<cmd>lua vim.diagnostic.open_float()<cr>", opts)
			vim.keymap.set("n", ")", "<cmd>lua vim.diagnostic.goto_next()<cr>", opts)
			vim.keymap.set("n", "(", "<cmd>lua vim.diagnostic.goto_prev()<cr>", opts)
			-- vim.keymap.set({'n', 'x'}, '<leader><Tab>', '<cmd>lua vim.lsp.buf.format({async = true})<cr>', opts)
			vim.keymap.set("n", "<leader> ", "<cmd>lua vim.lsp.buf.code_action()<cr>", opts)
		end,
	},
	{
		"stevearc/conform.nvim",
		config = function()
			require("conform").setup({
				formatters_by_ft = {
					lua = { "stylua" },
					python = { "isort", "black" },
				},
			})
			vim.keymap.set({ "n", "v" }, "<leader>f", function()
				require("conform").format()
			end, opts)
		end,
	},
	{
		"zapling/mason-conform.nvim",
		config = function()
			require("mason-conform").setup()
		end,
	},
	{
		"nvim-treesitter/nvim-treesitter-context",
		config = function()
			require("treesitter-context").setup({ enable = true })
		end,
	},
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
