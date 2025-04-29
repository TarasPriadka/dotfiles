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
3. VS Code hold and repeat keys command: `defaults write com.microsoft.VSCode ApplePressAndHoldEnabled -bool false`

## Setup Github
- [Setup SSH Key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
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
  1. Enable commit signing with `git config --global commit.gpgsign true`
  2. Add `export GPG_TTY=$(tty)` to the `.zshrc`
  3. Run `gpg --full-generate-key` with defaults
  4. Run `gpg --list-secret-keys --keyid-format=long` and copy id after `rsa3072/`
  5. Print key with `gpg --armor --export`
  6. Add to Github
     
## Apps to get
- [Spotify](https://download.scdn.co/SpotifyInstaller.zip)
- [Firefox](https://www.mozilla.org/en-US/firefox/mac/)/Arc
- [VS Code](https://code.visualstudio.com/docs?dv=osx)
- [Raycast](https://www.raycast.com/#)
- [Iterm2](https://iterm2.com/downloads/stable/latest)
- [Slack](https://slack.com/downloads/instructions/mac)
- [Zoom](https://zoom.us/download)
- [Notion](https://www.notion.so/desktop/apple-silicon/download)

## Mac Extensions
- [Flycut]
- [Rectangle](https://github.com/rxhanson/Rectangle/releases/download/v0.68/Rectangle0.68.dmg)
- [Hidden Bar](https://apps.apple.com/us/app/hidden-bar/id1452453066?mt=12)
- [Shottr](https://shottr.cc/)



## Extensions
- [uBlock Origin](https://chrome.google.com/webstore/detail/ublock-origin/cjpalhdlnbpafiamejdnhcphjbkeiagm)
- [Vimium-C](https://chrome.google.com/webstore/detail/vimium-c-all-by-keyboard/hfjbmagddngcpeloejdejnfgbamkjaeg)
- [I still don't care about cookies](https://chrome.google.com/webstore/detail/i-still-dont-care-about-c/edibdbjcniadpccecjdfdjjppcpchdlm)
