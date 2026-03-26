# Path to your oh-my-zsh installation.
export ZSH="$HOME/.oh-my-zsh"

zstyle ':omz:update' mode auto

autoload -Uz vcs_info
precmd() { vcs_info }

zstyle ':vcs_info:git:*' formats '%b'
zstyle ':vcs_info:*' enable git

git_prompt_info() {
  [[ -n "$vcs_info_msg_0_" ]] && echo "${vcs_info_msg_0_}" | sed 's/\*$//'
}

PROMPT='%F{blue}(%m)%f %F{green}%~%f %F{yellow}$(git_prompt_info)%f '

#Save up to 100000 entries in history file
SAVEHIST=100000
HISTSIZE=100000

setopt EXTENDED_HISTORY
setopt APPEND_HISTORY
setopt INC_APPEND_HISTORY
setopt SHARE_HISTORY
setopt HIST_EXPIRE_DUPS_FIRST
setopt HIST_IGNORE_DUPS
setopt HIST_FIND_NO_DUPS
setopt HIST_REDUCE_BLANKS

plugins=(zsh-autosuggestions web-search copyfile copypath zsh-syntax-highlighting)

source $ZSH/oh-my-zsh.sh

if [[ -n $SSH_CONNECTION ]]; then
  export EDITOR='vim'
else
  export EDITOR='vim'
fi

[ -f ~/.fzf.zsh ] && source ~/.fzf.zsh

# -------------- SSH Agent startup --------------

SSH_ENV="$HOME/.ssh/agent-environment"

function start_agent {
    echo "Initialising new SSH agent..."
    /usr/bin/ssh-agent | sed 's/^echo/#echo/' > "${SSH_ENV}"
    chmod 600 "${SSH_ENV}"
    . "${SSH_ENV}" > /dev/null
    /usr/bin/ssh-add;
}

if [ -f "${SSH_ENV}" ]; then
    . "${SSH_ENV}" > /dev/null
    ps -ef | grep ${SSH_AGENT_PID} | grep ssh-agent$ > /dev/null || {
        start_agent;
    }
else
    start_agent;
fi

# --------------------------------------------------

# -- pyenv --

export PYENV_ROOT="$HOME/.pyenv"
[[ -d $PYENV_ROOT/bin ]] && export PATH="$PYENV_ROOT/bin:$PATH"
eval "$(pyenv init - zsh)"
eval "$(pyenv virtualenv-init -)"

# -- pyenv --

export PATH="$HOME/.local/bin:$PATH"

alias k="kubectl"
alias python="python3"
alias gc="git checkout"
alias gr="git rebase"
alias gb="git branch"
alias gp="git push"
alias claer="clear"

export GPG_TTY=$(tty)
