# Setup Env

An attempt to simplify new computer setup with predefined vimrc, zshrc, and a script to set everything up.

## Common Setup

1. Install Oh-My-ZSH:
```
sh -c "$(curl -fsSL https://raw.github.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
```

2. Setup p10k ZSH theme
```
git clone --depth=1 https://github.com/romkatv/powerlevel10k.git ~/powerlevel10k
echo 'source ~/powerlevel10k/powerlevel10k.zsh-theme' >>~/.zshrc

exec zsh

p10k configure
```

3. Run installation script from this repo
```
sh -c "$(curl -fsSL https://raw.githubusercontent.com/TarasPriadka/setup_env/main/setup.sh)"
```

Useful Links and Tips:
1. Setup Iterm2 skips: `https://apple.stackexchange.com/questions/136928/using-alt-cmd-right-left-arrow-in-iterm`
2. Check Unix system version: `uname -r`
