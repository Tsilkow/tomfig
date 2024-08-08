set nocompatible " required for vundle
filetype off " required for vundle

" set rtp+=~/.vim/bundle/Vundle.vim
" call vundle#begin()
" 
" Plugin 'VundleVim/Vundle.vim'
" Plugin 'dracula/vim', { 'as': 'dracula' }
" Plugin 'terryma/vim-expand-region'
" 
" call vundle#end()
" filetype plugin indent on " required for vundle

set scrolloff=1

set ignorecase " case insensitive search
set smartcase " If there are uppercase letters, become case-sensitive.
set incsearch " live incremental searching
" set showmatch " live match highlighting
" set hlsearch " highlight matches
set gdefault " use the `g` flag by default.

set virtualedit=onemore " Allow moving one character past the end of the line.

set relativenumber
set tabstop=4
set shiftwidth=4
set softtabstop=4
set expandtab " use spaces instead of tabs.
set smarttab " let's tab key insert 'tab stops', and bksp deletes tabs.
set shiftround " tab / shifting moves to closest tabstop.
set autoindent " Match indents on new lines.
set smartindent " Intellegently dedent / indent new lines based on rules.

" Use the clipboard to copy and paste between Vim and other programs.
" set clipboard+=unnamed  " use the clipboards of vim and win
" set paste               " Paste from a windows or from vim
" set go+=a

" Don't use Ex mode, use Q for formatting.
map Q gq

noremap <Space> <Nop>
" nnoremap <C-Space> i
nnoremap <CR> i
let mapleader=" "

" nnoremap q q
nnoremap w c
nnoremap e <Nop>
nnoremap r R
noremap t .
" inoremap <C-y> <C-o>:action copilot.requestCompletion<CR>
noremap u b
inoremap <C-u> <C-o>b
inoremap <C-i> <C-o>w
noremap U B
noremap i w
noremap I W
noremap o %
noremap O %
noremap p J

nnoremap <Tab> >>
vnoremap <Tab> >gv
nnoremap <S-Tab> <<
vnoremap <S-Tab> <gv
nnoremap <leader><Tab> ==
vnoremap <leader><Tab> =gv
noremap a <Plug>(expand_region_expand)
noremap A <Plug>(expand_region_shrink)
nnoremap s v
nnoremap S V
noremap d "_x
inoremap <C-d> <C-o>"_x
noremap D "_X
inoremap <C-D> <C-o>"_X
noremap <leader>d "_dd
" noremap f f
" noremap F F
" noremap g g
inoremap <C-h> <Left>
noremap <leader>h ^
inoremap <C-j> <Down>
noremap <leader>j }
inoremap <C-k> <Up>
noremap J <C-d>
noremap <leader>k {
inoremap <C-l> <Right>
noremap K <C-u>
noremap <leader>l $
noremap ; ;
noremap : :
nnoremap <leader><CR> o
" nnoremap <S-CR> O

noremap z u
noremap Z U
noremap <leader>z <C-r>
noremap x d
noremap <leader>x "+d
noremap c y
noremap <leader>c "+y
noremap v p
noremap <leader>v "+p
cnoremap <c-v> <c-r>0
noremap V P
noremap <leader>V "+P
noremap b g;
noremap B g,
" noremap n n
noremap m <Nop>
noremap <leader>m <Nop>
noremap , <Nop>
noremap . <Nop>
" noremap / /
" noremap ? ?

noremap <Up> <Nop>
noremap <Down> <Nop>
noremap <Left> <Nop>
noremap <Right> <Nop>

" keybinding todo:
" * comments (`leader /` ?)
"
" neovim todo:
" * a -- expand, shrink region
" * e -- Nerdtree equivalent
" * m -- jump to definition/usage
" * <leader>m -- rename
" * , -- show parameters
" * . -- show error
