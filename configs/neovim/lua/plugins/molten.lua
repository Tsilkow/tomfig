return {
{
    'jmbuhr/otter.nvim',
    -- enabled=false,
    dev = false,
    dependencies = {
        'neovim/nvim-lspconfig',
        'nvim-treesitter/nvim-treesitter',
    },
    ft = { 'markdown', 'quarto' },
    opts = {
        verbose = {
            no_code_found = false,
        }
    },
},
{
    'quarto-dev/quarto-nvim',
    -- enabled=false,
    ft = {'quarto', 'markdown'},
    config = function()
        require('quarto').setup({
            lspFeatures = {
                languages = { "python" },
                chunks = "all",
                diagnostics = {
                    enabled = true,
                    triggers = { "BufWritePost" },
                },
                completion = {
                    enabled = true,
                },
            },
            keymap = {
                -- NOTE: setup your own keymaps:
                hover = ",",
                definition = "gd",
                rename = "<leader>r",
                references = "gr",
                format = "<leader><tab>",
            },
            codeRunner = {
                enabled = true,
                default_method = "molten",
            },
        })
        local runner = require("quarto.runner")
        vim.keymap.set("n", "<localleader>e", runner.run_cell,  { desc = "run cell", silent = true })
        vim.keymap.set("n", "<localleader>w", runner.run_all,   { desc = "run all cells", silent = true })
        vim.keymap.set("v", "<localleader>e",  runner.run_range, { desc = "run visual range", silent = true })
    end,
    dependencies = {
        "nvim-treesitter/nvim-treesitter",
        'jmbuhr/otter.nvim',
    },
},
{
    'GCBallesteros/jupytext.nvim',
    -- enabled=false,
    config = function()
        require('jupytext').setup({
            custom_language_formatting = {
                python = {
                    extension = "md",
                    style = "markdown",
                    force_ft = "markdown", -- you can set whatever filetype you want here
                },
            }
        })
    end
},
{
	'3rd/image.nvim',
    config = function()
    	require('image').setup({
            backend = "kitty",
            integrations = {
                markdown = {
                    enabled = true,
                    clear_in_insert_mode = false,
                    download_remote_images = true,
                    only_render_image_at_cursor = false,
                    filetypes = { "markdown", "vimwiki" }, -- markdown extensions (ie. quarto) can go here
                }
            },
            max_width = 100,
            max_height = 12,
            max_height_window_percentage = math.huge,
            max_width_window_percentage = math.huge,
            window_overlap_clear_enabled = true,
            window_overlap_clear_ft_ignore = { "cmp_menu", "cmp_docs", "" },
        })
    end,
    dependencies = {
      'leafo/magick',
    },
},
{
	'benlubas/molten-nvim',
    -- enabled=false,
    dependencies = { "3rd/image.nvim" },
    build = ":UpdateRemotePlugins",
    init = function()
        vim.g.molten_image_provider = "image.nvim"
        vim.g.molten_output_win_max_height = 20
        vim.g.molten_virt_lines_off_by_1 = true
    end,
    -- config = function()
    --     require('molten-nvim').setup({})
    -- end
},
}
