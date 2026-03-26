# Setup Env

An attempt to simplify new computer setup with predefined vimrc, zshrc, and a script to set everything up.

## Install (Linux)

```bash
curl -fsSL https://raw.githubusercontent.com/TarasPriadka/dotfiles/main/setup.sh | bash
```

The script will:
- Install system packages: zsh, tmux, fzf, ripgrep, bat, vim, tig, pyenv build deps
- Install fzf (from git), pyenv, oh-my-zsh, zsh plugins
- Create `~/code/`
- Download and place zshrc, gitconfig, vimrc, tmux.conf
- Generate SSH auth key (`~/.ssh/id_ed25519`) and signing key (`~/.ssh/ssh_sign`)
- Prompt for your name/email and configure git

After running, add both keys to GitHub and run `exec zsh`.

## Useful Links and Tips:
1. Setup Iterm2 skips: `https://apple.stackexchange.com/questions/136928/using-alt-cmd-right-left-arrow-in-iterm`
2. Check Unix system version: `uname -r`
3. VS Code hold and repeat keys command: `defaults write com.microsoft.VSCode ApplePressAndHoldEnabled -bool false`
4. Use `git update-index --skip-worktree FILE` to keep file changes out of the git worktree. Useful if you change some configs locally, but don't want to update upstream.

## Setup Github
- [Setup SSH Key](https://docs.github.com/en/authentication/connecting-to-github-with-ssh/generating-a-new-ssh-key-and-adding-it-to-the-ssh-agent)
  1. `ssh-keygen -t ed25519 -C "your_email@example.com"` — auth key
  2. `ssh-keygen -t ed25519 -C "your_email@example.com-signing" -f ~/.ssh/ssh_sign` — signing key
  3. `touch ~/.ssh/config` and add:
  ```
  Host github.com
  AddKeysToAgent yes
  UseKeychain yes
  IdentityFile ~/.ssh/id_ed25519
  ```
  4. Go to the Github settings and paste in the public key that you have generated

- Setup SSH commit signing
  1. `git config --global gpg.format ssh`
  2. `git config --global user.signingkey ~/.ssh/ssh_sign`
  3. `git config --global commit.gpgsign true`

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
