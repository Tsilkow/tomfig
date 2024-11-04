local opts = {
    spelllang = 'en_us,pl',
    spell = true,
}

colorscheme_name = 'rose-pine'

for opt, val in pairs(opts) do
	vim.o[opt] = val
end

-- Fetch and setup colorscheme if available, otherwise just return 'default'
-- This should prevent Neovim from complaining about missing colorschemes on first boot
local function get_if_available(name, opts)
	local lua_ok, colorscheme = pcall(require, name)
	if lua_ok then
		colorscheme.setup(opts)
		return name
	end

	local vim_ok, _ = pcall(vim.cmd.colorscheme, name)
	if vim_ok then
		return name
	end

	return "default"
end

local colorscheme = get_if_available(colorscheme_name)
vim.cmd.colorscheme(colorscheme)

vim.g.python3_host_prog=vim.fn.expand("~/.venvs/nvim/bin/python3")

