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

## Useful Links and Tips:
1. Setup Iterm2 skips: `https://apple.stackexchange.com/questions/136928/using-alt-cmd-right-left-arrow-in-iterm`
2. Check Unix system version: `uname -r`

## Setup Github
- Setup SSH Key
  1. `ssh-keygen -t ed25519 -C "your_email@example.com"`
  2. `touch ~/.ssh/config`
  3. Add key to the config: `vim ~/.ssh/config`
  ```
  Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519
  ```
  4. Go to the Github settings and paste in the public key that you have generated

- Setup GPG Key

## Apps to get
- [Spotify](https://download.scdn.co/SpotifyInstaller.zip)
- [Firefox](https://www.mozilla.org/en-US/firefox/mac/)/Arc
- [VS Code](https://code.visualstudio.com/docs?dv=osx)
- [Raycast](https://www.raycast.com/#)
- [Iterm2](https://iterm2.com/downloads/stable/latest)
- [Rectangle](https://github.com/rxhanson/Rectangle/releases/download/v0.68/Rectangle0.68.dmg)
- [Slack](https://slack.com/downloads/instructions/mac)
- [Hidden Bar](https://apps.apple.com/us/app/hidden-bar/id1452453066?mt=12)
- [Zoom](https://zoom.us/download)
- [Shottr](https://shottr.cc/)
- [Notion](https://www.notion.so/desktop/apple-silicon/download)

