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

# install golang
wget -O https://go.dev/dl/go1.18.4.linux-amd64.tar.gz
rm -rf /usr/local/go && tar -C /usr/local -xzf go1.18.4.linux-amd64.tar.gz
export PATH=$PATH:/usr/local/go/bin

# install rust
curl --proto '=https' --tlsv1.2 -sSf https://sh.rustup.rs | sh

# install python
apt-get install python
apt-get install pip

# Copy vimrc and zshrc files to home
curl -O $GIT_REPO/$VIMRC_PATH 
curl -O $GIT_REPO/$ZSHRC_PATH 

cp  $VIMRC_PATH ~/.vimrc
cp  $ZSHRC_PATH ~/.zshrc

rm $VIMRC_PATH
rm $ZSHRC_PATH
