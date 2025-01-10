return {
  {
    "nvim-treesitter/nvim-treesitter",
    version = false, -- last release is way too old and doesn't work on windows
    build = ":tsupdate",
    config = function ()
      local configs = require("nvim-treesitter.configs")

      configs.setup({
        ensure_installed = {
          "bash",
          "cpp",
          "diff",
          "dockerfile",
          "go",
          "html",
          "javascript",
          "json",
          "lua",
          "luadoc",
          "luap",
          "markdown",
          "markdown_inline",
          "printf",
          "python",
          "query",
          "regex",
          "toml",
          "vim",
          "vimdoc",
          "xml",
          "yaml",
        },
        sync_install = false,
        highlight = { enable = true },
        indent = { enable = true },
        incremental_selection = {
          enable = true,
          keymaps = {
            node_incremental = "s",
            node_decremental = "S",
          },
        },
        textobjects = {
          move = {
            enable = true,
            set_jumps = false, -- you can change this if you want.
            goto_next_start = {
              --- ... other keymaps
              ["]b"] = { query = "@code_cell.inner", desc = "next code block" },
            },
            goto_previous_start = {
              --- ... other keymaps
              ["[b"] = { query = "@code_cell.inner", desc = "previous code block" },
            },
          },
          select = {
            enable = true,
            lookahead = true, -- you can change this if you want
            keymaps = {
              --- ... other keymaps
              ["sb"] = { query = "@code_cell.inner", desc = "in block" },
              ["ab"] = { query = "@code_cell.outer", desc = "around block" },
            },
          },
          swap = { -- Swap only works with code blocks that are under the same
            -- markdown header
            enable = true,
            swap_next = {
              --- ... other keymap
              ["<leader>sbl"] = "@code_cell.outer",
            },
            swap_previous = {
              --- ... other keymap
              ["<leader>sbh"] = "@code_cell.outer",
            },
          },
        }
      })
    end
  },
  {
    "nvim-treesitter/nvim-treesitter-textobjects",
  },
  {
    "HiPhish/rainbow-delimiters.nvim",
  },
}

