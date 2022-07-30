#!/bin/sh

if [[ "$OSTYPE" == "linux-gnu"* ]]; then
    # install zsh
    sudo apt install zsh -y
elif [[ "$OSTYPE" == "darwin"* ]]; then
    # install xcode command line utilities needed for homebrew
    xcode-select --install

    # install HomeBrew manager
    /bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

    # install zsh
    brew install zsh
else
    echo "Unknown system. Not sure how to setup. Exiting..."
    exit 1
fi

chsh -s $(which zsh)

# Copy vimrc and zshrc files to home
cp ./vimrc ~/.vimrc
cp ./zshrc ~/.zshrc

git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k
echo 'source ~/powerlevel10k/powerlevel10k.zsh-theme' >>~/.zshrc

exec zsh

p10k configure

