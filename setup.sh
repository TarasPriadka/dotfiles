#!/usr/bin/env bash
set -euo pipefail

REPO="TarasPriadka/dotfiles"
RAW_BASE="https://raw.githubusercontent.com/$REPO/main"

GREEN='\033[0;32m'
YELLOW='\033[1;33m'
CYAN='\033[0;36m'
NC='\033[0m'

info()    { echo -e "${CYAN}[setup]${NC} $*"; }
success() { echo -e "${GREEN}[setup]${NC} $*"; }
warn()    { echo -e "${YELLOW}[setup]${NC} $*"; }

# ── System packages ────────────────────────────────────────────────────────
info "Installing system packages..."
sudo apt-get install -y \
    zsh git curl vim tmux ripgrep tig

# ── oh-my-zsh ─────────────────────────────────────────────────────────────
if [ ! -d "$HOME/.oh-my-zsh" ]; then
    info "Installing oh-my-zsh..."
    RUNZSH=no CHSH=no sh -c "$(curl -fsSL https://raw.githubusercontent.com/ohmyzsh/ohmyzsh/master/tools/install.sh)"
    success "Installed oh-my-zsh"
else
    info "oh-my-zsh already installed, skipping"
fi

# ── fzf ────────────────────────────────────────────────────────
if [ ! -d "$HOME/.fzf" ]; then
    info "Installing fzf from git..."
    git clone --depth 1 https://github.com/junegunn/fzf.git "$HOME/.fzf"
    "$HOME/.fzf/install" --all < /dev/tty
    success "Installed fzf"
else
    info "fzf already installed, skipping"
fi

# ── pyenv ──────────────────────────────────────────────────────────────────
if [ ! -d "$HOME/.pyenv" ]; then
    info "Installing pyenv..."
    curl -fsSL https://pyenv.run | bash
    success "Installed pyenv"
else
    info "pyenv already installed, skipping"
fi


# ── zsh plugins ────────────────────────────────────────────────────────────
ZSH_CUSTOM="${ZSH_CUSTOM:-$HOME/.oh-my-zsh/custom}"

if [ ! -d "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting" ]; then
    info "Installing zsh-syntax-highlighting..."
    git clone https://github.com/zsh-users/zsh-syntax-highlighting.git \
        "$ZSH_CUSTOM/plugins/zsh-syntax-highlighting"
fi

if [ ! -d "$ZSH_CUSTOM/plugins/zsh-autosuggestions" ]; then
    info "Installing zsh-autosuggestions..."
    git clone https://github.com/zsh-users/zsh-autosuggestions \
        "$ZSH_CUSTOM/plugins/zsh-autosuggestions"
fi

# ── ~/code directory ───────────────────────────────────────────────────────
mkdir -p "$HOME/code"

# ── Config files ───────────────────────────────────────────────────────────
info "Downloading config files..."
curl -fsSL "$RAW_BASE/zshrc"    -o "$HOME/.zshrc"
curl -fsSL "$RAW_BASE/gitconfig" -o "$HOME/.gitconfig"
curl -fsSL "$RAW_BASE/vimrc"     -o "$HOME/.vimrc"
curl -fsSL "$RAW_BASE/tmux.conf" -o "$HOME/.tmux.conf"
success "Config files placed in ~/"

# ── SSH keys ───────────────────────────────────────────────────────────────
mkdir -p "$HOME/.ssh"
chmod 700 "$HOME/.ssh"

# Prompt for email to embed in key comments (used later for git config too)
echo ""
read -r -p "Enter your email (for SSH key comments and git config): " USER_EMAIL </dev/tty
read -r -p "Enter your full name (for git config): " USER_NAME </dev/tty

if [ ! -f "$HOME/.ssh/id_ed25519" ]; then
    info "Generating SSH auth key (~/.ssh/id_ed25519)..."
    ssh-keygen -t ed25519 -C "$USER_EMAIL" -f "$HOME/.ssh/id_ed25519" -N ""
    success "Generated auth key"
else
    info "~/.ssh/id_ed25519 already exists, skipping"
fi

if [ ! -f "$HOME/.ssh/ssh_sign" ]; then
    info "Generating SSH signing key (~/.ssh/ssh_sign)..."
    ssh-keygen -t ed25519 -C "${USER_EMAIL}-signing" -f "$HOME/.ssh/ssh_sign" -N ""
    success "Generated signing key"
else
    info "~/.ssh/ssh_sign already exists, skipping"
fi

# SSH config — add GitHub entry if not present
SSH_CONFIG="$HOME/.ssh/config"
touch "$SSH_CONFIG"
chmod 600 "$SSH_CONFIG"
if ! grep -q "Host github.com" "$SSH_CONFIG" 2>/dev/null; then
    cat >> "$SSH_CONFIG" <<'EOF'

Host github.com
    AddKeysToAgent yes
    IdentityFile ~/.ssh/id_ed25519
EOF
    success "Added GitHub entry to ~/.ssh/config"
fi

# ── Git user config ───────────────────────────────────────────────────────
git config --global user.name "$USER_NAME"
git config --global user.email "$USER_EMAIL"
success "Git user config set"

# ── Change default shell to zsh ──────────────────────────────────────────
if [ "$SHELL" != "$(which zsh)" ]; then
    info "Changing default shell to zsh..."
    chsh -s "$(which zsh)"
    success "Default shell changed to zsh"
fi

# ── Done ──────────────────────────────────────────────────────────────────────
echo ""
echo -e "${GREEN}════════════════════════════════════════════════════${NC}"
echo -e "${GREEN}  Setup complete!${NC}"
echo -e "${GREEN}════════════════════════════════════════════════════${NC}"
echo ""
echo -e "${YELLOW}MANUAL STEPS REQUIRED:${NC}"
echo ""
echo "1. Add your SSH AUTH key to GitHub:"
echo "   https://github.com/settings/ssh/new  (Key type: Authentication Key)"
echo ""
echo "   $(cat "$HOME/.ssh/id_ed25519.pub")"
echo ""
echo "2. Add your SSH SIGNING key to GitHub:"
echo "   https://github.com/settings/ssh/new  (Key type: Signing Key)"
echo ""
echo "   $(cat "$HOME/.ssh/ssh_sign.pub")"
echo ""
echo "3. Restart your shell:"
echo "   exec zsh"
echo ""
