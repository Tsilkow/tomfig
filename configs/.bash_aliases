# .bash_aliases

function venv () {
    source "$1/bin/activate"
}

function gic () {
    git commit -m "$1" 
}

function tma () {
    tmux a -t "$1"
}

function dex () {
    docker exec -ti "$1" bash
}

alias sudo='sudo '

alias gis='git status'

alias gid='git diff'

alias giau='git add -u'

alias tmls='tmux ls'

alias tmcp='tmux show-buffer | xclip -selection clipboard'

alias dps='docker ps'
