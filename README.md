# Setup Env

## Install (Linux)

```bash
curl -fsSL https://raw.githubusercontent.com/TarasPriadka/dotfiles/main/setup.sh | bash
```

The script will:
- Install system packages
- Install fzf (from git), pyenv, oh-my-zsh, zsh plugins
- Create `~/code/`
- Download and place zshrc, gitconfig, vimrc, tmux.conf
- Generate SSH auth key (`~/.ssh/id_ed25519`) and signing key (`~/.ssh/ssh_sign`)
- Prompt for your name/email and configure git
- Install the `night` and `coin` terminal programs in `~/.local/bin/`

After running, add both keys to GitHub and run `exec zsh`.

## Personal Codex skills

This repo keeps personal skills under `skills/<skill-name>/SKILL.md`. Install
them on any Linux machine without cloning the repo:

```bash
curl -fsSL https://raw.githubusercontent.com/TarasPriadka/dotfiles/main/skills/install.sh | bash
```

The installer downloads the public repo archive, keeps only its skill folders
under `~/.local/share/dotfiles-skills/`, and links them into
`~/.agents/skills/`. An hourly user-level systemd timer downloads a fresh
archive and updates that cache. It does not need a Git checkout. Existing
skills with the same names are left alone unless they were installed by this
script. Codex discovers the linked skills from any local repo. If an updated
skill does not appear immediately, restart Codex.

The main `setup.sh` downloads and runs this installer as part of setup.

## Terminal programs

`night` shows a moonlit railway scene, and `coin` renders a rotating ASCII
GIMLET coin. Both are Python 3.9+ programs with no third party packages. Their
source lives in `programs/` and the Linux setup script installs them in
`~/.local/bin/`. Open a new shell after setup so the commands are on `PATH`.

To install or update only these programs:

```bash
curl -fsSL https://raw.githubusercontent.com/TarasPriadka/dotfiles/main/programs/install.sh | bash
```

For a single plain frame, run `night --frames 1 --no-color` or
`coin --frames 1 --no-color`.

## Sync Configs Only

Already have the tools installed and just want to pull the latest configs?

```bash
curl -fsSL https://raw.githubusercontent.com/TarasPriadka/dotfiles/main/zshrc    -o ~/.zshrc
curl -fsSL https://raw.githubusercontent.com/TarasPriadka/dotfiles/main/gitconfig -o ~/.gitconfig
curl -fsSL https://raw.githubusercontent.com/TarasPriadka/dotfiles/main/vimrc     -o ~/.vimrc
curl -fsSL https://raw.githubusercontent.com/TarasPriadka/dotfiles/main/tmux.conf -o ~/.tmux.conf
```

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
