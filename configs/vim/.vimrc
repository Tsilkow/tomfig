set nocompatible 

set autoindent " Match indents on new lines.
set colorcolumn=80,100
set expandtab " use spaces instead of tabs.
set gdefault " use the `g` flag by default.
set history=1000
set hlsearch " highlight search
set ignorecase " case insensitive search
set incsearch
set number
set relativenumber
set scrolloff=5
set shiftround " tab / shifting moves to closest tabstop.
set shiftwidth=4
set showmatch
set smartcase
set smartindent " Intellegently dedent / indent new lines based on rules.
set smarttab " let's tab key insert 'tab stops', and bksp deletes tabs.
set softtabstop=4
set tabstop=4
set termguicolors
set virtualedit=onemore " Allow moving one character past the end of the line.
set wildmode=list:longest,list:full
set wrap

" Don't use Ex mode, use Q for formatting.
map Q gq

noremap <Space> <Nop>
nnoremap <CR> i
let mapleader=" "

" nnoremap q q
nnoremap w <C-w><C-w>
nnoremap e <Nop>
nnoremap r R
noremap t <Nop>
" inoremap <C-y> <C-o>:action copilot.requestCompletion<CR>
noremap u b
inoremap <C-u> <C-o>b
noremap U B
noremap i e
inoremap <C-i> <C-o>e
noremap I E
noremap o w
noremap O W
noremap p %
noremap P J

inoremap <Tab> <C-v><Tab>
nnoremap <Tab> >>
vnoremap <Tab> >gv
nnoremap <S-Tab> <<
vnoremap <S-Tab> <gv
nnoremap <leader><Tab> ==
vnoremap <leader><Tab> =gv
" reserved for expand/shrink selection
noremap a <Nop>
noremap A <Nop>
nnoremap s v
nnoremap S V
noremap d "_d
inoremap <C-d> <C-o>"_x
noremap D "_x
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
" noremap ; ;
" noremap : :
" reserved for commenting
noremap ' <Nop>
nnoremap <leader><CR> o
nnoremap OM A

noremap z u
noremap Z U
noremap <leader>z <C-r>
noremap x d
noremap X D
noremap <leader>x "+d
noremap c y
noremap <leader>c "+y
noremap v p
noremap V P
noremap <leader>v "+p
noremap <leader>V "+P
cnoremap <c-v> <c-r>0
" reserved for buffer actions
noremap b :b <C-d> 
noremap B <Nop>
" noremap n n
noremap m '
noremap <leader>m m
" reserved for show parameters
noremap , <Nop>
" noremap . .
" noremap / /
" noremap ? ?

noremap <Up> <Nop>
noremap <Down> <Nop>
noremap <Left> <Nop>
noremap <Right> <Nop>
