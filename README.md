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
- Install `night`, `coin`, `beach`, `git-uncommit`, and `git-review` in `~/.local/bin/`

After running, add both keys to GitHub and run `exec zsh`.

## Personal Codex workflow

Install the default working guide and personal skills on a Linux machine without
cloning this repository:

```bash
curl -fsSL https://raw.githubusercontent.com/TarasPriadka/dotfiles/main/skills/install.sh | bash
```

The normal `setup.sh` already runs this installer. On an existing machine, rerun
the command once to upgrade the old skills-only updater.

The installer links `~/.codex/AGENTS.md` and `~/.agents/skills/` to a shared release
under `~/.local/share/dotfiles-skills/`. New Codex sessions receive the ownership
and collaboration defaults automatically and select `engineering-work` for
substantive tasks. You can describe the task normally without naming skills.
The working method covers investigation, design, simplification, execution,
verification, delivery, and durable work records when needed.

An hourly user-level systemd timer updates the guide and skills from the same
archive. A failed download or incomplete framework leaves the prior release
active. The old dotfiles checkout pilot links are migrated together. Unrelated
personal guides, overrides, or conflicting `engineering-work` installations are
preserved and reported as conflicts; other custom skills are left alone.

For a custom Codex directory, set `DOTFILES_CODEX_HOME` when installing. The
updater remembers it for subsequent timer runs. `CODEX_HOME` is used on the
first normal installation when no saved location exists. Restart Codex after
installing to load the new default guide.

See [the framework guide](agents/README.md) for development and evaluation.

## Terminal programs

`night` shows a moonlit railway scene, `coin` renders a rotating ASCII
GIMLET coin, and `beach` shows a warm ocean scene with rolling waves and
swaying green palms. All three are Python 3.9+ programs with no third party
packages. Their
source lives in `programs/` and the Linux setup script installs them in
`~/.local/bin/`. Open a new shell after setup so the commands are on `PATH`.
`night` starts with its status and controls hidden; press `i` to show them or
`h` for help.

To install or update these programs and the Git helper aliases:

```bash
curl -fsSL https://raw.githubusercontent.com/TarasPriadka/dotfiles/main/programs/install.sh | bash
```

Start a quiet beach background with:

```bash
beach --eco --hide-hud
beach --mood golden
```

`beach` defaults to 8 FPS; `--eco` caps it at 4 FPS. Press `1`–`3` to change
moods, `w` for waves, `b` for wind, `t` for colors, Space to pause, and `q` to
quit. Press `h` for all controls, or run `beach --help` for startup options.
It caches scenery and palm shapes and sends only changed cells to the terminal.

For a single plain frame, pipe any program to a file, for example
`beach --frames 1 > beach.txt`. All three also accept `--no-color`.

## Switching reviews with git review

`git review` replaces the previous staged review with the latest remote branch's
PR diff. It fetches the head and base before cleanup, accepts force-pushed history,
and leaves the combined change staged for review in your editor.

```bash
git review someone/branch       # Switch to and prepare this branch
git review                      # Refresh the current review after a push
git review feature --base main  # Specify a remote base without GitHub lookup
```

The command discards **all staged changes**, including staged additions and
deletions. It stops before cleanup if there are unstaged edits, an active Git
operation, or the target branch is checked out in another worktree. Untracked and
ignored files are preserved; conflicting paths stop the command before cleanup.
Failed PR lookups and fetches also leave the current review intact.

The local target branch is replaced with the fetched remote head, then soft-reset
to its merge base with the fetched PR base. Stacked PRs compare against their
parent. If the author's branch is behind its base, the command reports that;
it does not rebase, merge, or push. The fetched head is available in `ORIG_HEAD`
and the remote-tracking ref after the reset.

The remote defaults to the target branch's configured upstream remote, or
`origin`; use `--remote <name>` to override it. A configured upstream branch name
is respected. Automatic base lookup requires an authenticated GitHub CLI and a
PR whose head belongs to that remote's repository. Use `--base <remote-branch>`
for branches without a PR, non-GitHub remotes, or explicit fork comparisons.

Repeat reviews overlap the GitHub lookup and fetch using the previous base name
stored in `branch.<name>.reviewBase` as a hint. The PR base is still checked live
on every run; retargeting triggers a fetch of the new base before cleanup.
File protection skips unrelated untracked directories, including ignored build
and dependency trees, and inspects their contents only where a checkout could
overlap them.

Install or update with the programs installer below. New machines also get the
command through `setup.sh`.

## Uncommitting with git uncommit

`git uncommit` soft-resets the current branch to its common ancestor with the
PR's parent branch, leaving the branch's combined changes staged for review in
your editor. For a stack `main → A → B → C`, running it on C compares against B.
Existing staged, unstaged, untracked, and ignored files are preserved.

```bash
git uncommit                    # Use the current PR's parent branch
git uncommit --base local-parent # Specify a local parent ref without GitHub
git uncommit --one               # Uncommit only the latest commit without GitHub
```

`--one` soft-resets to the latest commit's first parent, preserving local edits
and leaving the uncommitted changes staged. Each invocation removes one commit;
it cannot be combined with `--base` and fails without changes at the root commit.

Automatic parent lookup requires an existing PR and an authenticated GitHub CLI
(`gh`). It uses the parent's local `origin/<branch>` ref; it does not fetch.
Run `git fetch origin` first if those refs need refreshing. If lookup fails, the
command stops; use `--base` to choose the parent explicitly.

There is no saved review state, restore mode, or cleanup. Old review metadata
is ignored. The command only moves the local branch pointer; it does not push.

To install or update (requires Git, Python 3, and curl):

```bash
curl -fsSL https://raw.githubusercontent.com/TarasPriadka/dotfiles/main/programs/install.sh | bash
```

The installer updates both helpers and their aliases in `~/.gitconfig`,
preserving your other Git settings. New machines get it through `setup.sh`.
Run `gh auth login` if GitHub CLI authentication is needed.

Run both helpers' tests without network access:

```bash
python3 -m unittest discover -s programs/tests -p 'test_git_*.py' -v
```

## Sync Configs Only

Already have the tools installed and just want to pull the latest configs?

```bash
curl -fsSL https://raw.githubusercontent.com/TarasPriadka/dotfiles/main/zshrc    -o ~/.zshrc
curl -fsSL https://raw.githubusercontent.com/TarasPriadka/dotfiles/main/gitconfig -o ~/.gitconfig
curl -fsSL https://raw.githubusercontent.com/TarasPriadka/dotfiles/main/vimrc     -o ~/.vimrc
curl -fsSL https://raw.githubusercontent.com/TarasPriadka/dotfiles/main/tmux.conf -o ~/.tmux.conf
curl -fsSL https://raw.githubusercontent.com/TarasPriadka/dotfiles/main/programs/install.sh | bash
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
