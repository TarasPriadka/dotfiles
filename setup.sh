#!/bin/sh

GIT_REPO="https://raw.githubusercontent.com/TarasPriadka/setup_env/main"
VIMRC_PATH="vimrc"
ZSHRC_PATH="zshrc"

cd $HOME

/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"
(echo; echo 'eval "$(/opt/homebrew/bin/brew shellenv)"') >> /Users/taras/.zprofile
eval "$(/opt/homebrew/bin/brew shellenv)"

brew install fzf
$(brew --prefix)/opt/fzf/install


git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# Copy vimrc and zshrc files to home
curl -O $GIT_REPO/$VIMRC_PATH
curl -O $GIT_REPO/$ZSHRC_PATH

cp  $VIMRC_PATH ~/.vimrc
cp  $ZSHRC_PATH ~/.zshrc

rm $VIMRC_PATH
rm $ZSHRC_PATH
