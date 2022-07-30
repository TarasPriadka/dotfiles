#!/bin/sh

GIT_REPO="https://raw.githubusercontent.com/TarasPriadka/setup_env/main"
VIMRC_PATH="vimrc"
ZSHRC_PATH="zshrc"

cd $HOME

# install code highlighting for zsh
git clone https://github.com/zsh-users/zsh-syntax-highlighting.git ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-syntax-highlighting

# install code completetion for zsh
git clone https://github.com/zsh-users/zsh-autosuggestions ${ZSH_CUSTOM:-~/.oh-my-zsh/custom}/plugins/zsh-autosuggestions

# install ag searcher
apt-get install silversearcher-ag

# install k9s
sudo apt-get install k9s -y

# Copy vimrc and zshrc files to home
curl -O $GIT_REPO/$VIMRC_PATH 
curl -O $GIT_REPO/$ZSHRC_PATH 

cp  $VIMRC_PATH ~/.vimrc
cp  $ZSHRC_PATH ~/.zshrc

rm $VIMRC_PATH
rm $ZSHRC_PATH

source ~/.zshrc
