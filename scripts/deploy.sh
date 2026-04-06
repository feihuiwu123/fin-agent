#!/bin/bash
# FinAgent One-Click Deploy Script
# Usage: bash deploy.sh
# Requirements: Ubuntu 22.04+ / Debian 12+

set -euo pipefail

# ==================== Color Output ====================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# ==================== Configuration (read from .env) ====================
# LLM Provider: deepseek / opencode / minimax / qwen / openrouter
LLM_PROVIDER="${LLM_PROVIDER:-deepseek}"
LLM_API_KEY="${LLM_API_KEY:-}"
LLM_API_BASE="${LLM_API_BASE:-}"
LLM_MODEL="${LLM_MODEL:-}"

# Auto-set defaults based on provider
if [ -z "$LLM_API_BASE" ]; then
    case "$LLM_PROVIDER" in
        deepseek)   LLM_API_BASE="https://api.deepseek.com/v1" ;;
        opencode)   LLM_API_BASE="https://api.opencode.ai/v1" ;;
        minimax)    LLM_API_BASE="https://api.minimax.chat/v1" ;;
        qwen)       LLM_API_BASE="https://dashscope.aliyuncs.com/compatible-mode/v1" ;;
        openrouter) LLM_API_BASE="https://openrouter.ai/api/v1" ;;
        *)          LLM_API_BASE="https://api.deepseek.com/v1" ;;
    esac
fi
if [ -z "$LLM_MODEL" ]; then
    case "$LLM_PROVIDER" in
        deepseek)   LLM_MODEL="deepseek/deepseek-chat" ;;
        opencode)   LLM_MODEL="opencode/default" ;;
        minimax)    LLM_MODEL="minimax/MiniMax-M1" ;;
        qwen)       LLM_MODEL="qwen/qwen-plus" ;;
        openrouter) LLM_MODEL="openrouter/auto" ;;
        *)          LLM_MODEL="deepseek/deepseek-chat" ;;
    esac
fi

# Channel configuration (optional, leave empty to disable)
FEISHU_ENABLED="${FEISHU_ENABLED:-false}"
FEISHU_APP_ID="${FEISHU_APP_ID:-}"
FEISHU_APP_SECRET="${FEISHU_APP_SECRET:-}"
FEISHU_CHAT_ID="${FEISHU_CHAT_ID:-}"
FEISHU_WEBHOOK_URL="${FEISHU_WEBHOOK_URL:-}"
WECHAT_ENABLED="${WECHAT_ENABLED:-false}"
DINGTALK_ENABLED="${DINGTALK_ENABLED:-false}"
DINGTALK_APP_KEY="${DINGTALK_APP_KEY:-}"
DINGTALK_APP_SECRET="${DINGTALK_APP_SECRET:-}"
QQ_ENABLED="${QQ_ENABLED:-false}"
QQ_APP_ID="${QQ_APP_ID:-}"
QQ_APP_SECRET="${QQ_APP_SECRET:-}"
EMAIL_ENABLED="${EMAIL_ENABLED:-false}"
EMAIL_IMAP_HOST="${EMAIL_IMAP_HOST:-imap.example.com}"
EMAIL_IMAP_PORT="${EMAIL_IMAP_PORT:-993}"
EMAIL_IMAP_USER="${EMAIL_IMAP_USER:-}"
EMAIL_IMAP_PASSWORD="${EMAIL_IMAP_PASSWORD:-}"
EMAIL_SMTP_HOST="${EMAIL_SMTP_HOST:-smtp.example.com}"
EMAIL_SMTP_PORT="${EMAIL_SMTP_PORT:-465}"
EMAIL_SMTP_USER="${EMAIL_SMTP_USER:-}"
EMAIL_SMTP_PASSWORD="${EMAIL_SMTP_PASSWORD:-}"
TELEGRAM_ENABLED="${TELEGRAM_ENABLED:-false}"
TELEGRAM_BOT_TOKEN="${TELEGRAM_BOT_TOKEN:-}"
DISCORD_ENABLED="${DISCORD_ENABLED:-false}"
DISCORD_BOT_TOKEN="${DISCORD_BOT_TOKEN:-}"
WHATSAPP_ENABLED="${WHATSAPP_ENABLED:-false}"
SLACK_ENABLED="${SLACK_ENABLED:-false}"
SLACK_BOT_TOKEN="${SLACK_BOT_TOKEN:-}"
SLACK_APP_TOKEN="${SLACK_APP_TOKEN:-}"

# Deploy path (prefer current directory if .env or .git exists)
if [ -f ".env" ] || [ -d ".git" ]; then
    DEPLOY_DIR="$(pwd)"
else
    DEPLOY_DIR="${DEPLOY_DIR:-$HOME/fin-agent}"
fi
VENV_DIR="${DEPLOY_DIR}/.venv"

# ==================== Pre-checks ====================
info "=== FinAgent Deploy Script ==="
info "Deploy directory: $DEPLOY_DIR"

# Load .env variables
if [ -f "$DEPLOY_DIR/.env" ]; then
    info "Loading .env variables..."
    set -a
    source "$DEPLOY_DIR/.env"
    set +a
elif [ -f ".env" ]; then
    info "Loading .env variables..."
    set -a
    source ".env"
    set +a
else
    warn ".env file not found, using environment variables or defaults"
fi

# Security check: prohibit root execution
if [ "$(id -u)" -eq 0 ]; then
    error "Running as root is not allowed! Please create a regular user to deploy\n  Example: useradd -m finagent && su - finagent"
fi

# Check sudo prerequisites (without triggering password prompt)
CURRENT_USER="$(whoami)"
if ! id -nG | grep -qw sudo; then
    error "User '$CURRENT_USER' is not in the sudo group!

Please switch to root and run the following to fix:
  su -
  # 1. Add user to sudo group
  usermod -aG sudo $CURRENT_USER
  # 2. Set a password for the user (required for sudo during deploy)
  passwd $CURRENT_USER
  # 3. Switch back to user and redeploy
  su - $CURRENT_USER
  bash scripts/deploy.sh"
fi

# Check system
if ! command -v apt &>/dev/null; then
    warn "Not a Debian/Ubuntu system, you may need to install dependencies manually"
fi

# ==================== 1. Install System Dependencies ====================
info "[1/7] Installing system dependencies..."

# Prefer detecting existing Python 3.11+
PYTHON=""
for ver in python3.13 python3.12 python3.11; do
    if command -v $ver &>/dev/null; then
        PYTHON=$ver
        break
    fi
done

if [ -z "$PYTHON" ]; then
    sudo apt update -qq
    for ver in 13 12 11; do
        info "Attempting to install python3.${ver}..."
        sudo apt install -y python3.${ver} python3.${ver}-venv python3-pip git curl 2>/dev/null && {
            PYTHON="python3.${ver}"
            break
        }
    done
    if [ -z "$PYTHON" ]; then
        error "Python 3.11+ installation failed, please install manually"
    fi
fi

info "Python version: $($PYTHON --version)"

# ==================== 2. Clone/Update Code ====================
info "[2/7] Preparing code..."
if [ -d "$DEPLOY_DIR/.git" ]; then
    cd "$DEPLOY_DIR"
    git pull
    info "Code is up to date"
else
    mkdir -p "$(dirname "$DEPLOY_DIR")"
    # If you have a git repo, uncomment and update the URL below
    # git clone https://github.com/yourname/finagent.git "$DEPLOY_DIR"
    info "Please copy code to $DEPLOY_DIR, or update the git clone URL in this script"
fi
cd "$DEPLOY_DIR"

# ==================== 3. Create Virtual Environment ====================
info "[3/7] Creating Python virtual environment..."
$PYTHON -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
pip install --upgrade pip -q

# ==================== 4. Install Python Dependencies ====================
info "[4/7] Installing Python dependencies..."
pip install -e ".[dev]" -q
pip install nanobot-ai -q
info "Dependencies installed"

# ==================== 5. Initialize Nanobot Configuration ====================
info "[5/7] Initializing Nanobot configuration..."
NANOBOT_CONFIG="$HOME/.nanobot/config.json"
mkdir -p "$HOME/.nanobot"

# Build channels JSON
CHANNELS_JSON="{"

# Feishu
CHANNELS_JSON+="\"feishu\": {\"enabled\": ${FEISHU_ENABLED}"
if [ -n "$FEISHU_APP_ID" ]; then
    CHANNELS_JSON+=", \"appId\": \"${FEISHU_APP_ID}\", \"appSecret\": \"${FEISHU_APP_SECRET}\""
fi
CHANNELS_JSON+="}"

# WeChat
CHANNELS_JSON+=", \"weixin\": {\"enabled\": ${WECHAT_ENABLED}}"

# DingTalk
CHANNELS_JSON+=", \"dingtalk\": {\"enabled\": ${DINGTALK_ENABLED}"
if [ -n "$DINGTALK_APP_KEY" ]; then
    CHANNELS_JSON+=", \"appKey\": \"${DINGTALK_APP_KEY}\", \"appSecret\": \"${DINGTALK_APP_SECRET}\""
fi
CHANNELS_JSON+="}"

# QQ
CHANNELS_JSON+=", \"qq\": {\"enabled\": ${QQ_ENABLED}"
if [ -n "$QQ_APP_ID" ]; then
    CHANNELS_JSON+=", \"appId\": \"${QQ_APP_ID}\", \"appSecret\": \"${QQ_APP_SECRET}\""
fi
CHANNELS_JSON+="}"

# Email
CHANNELS_JSON+=", \"email\": {\"enabled\": ${EMAIL_ENABLED}"
if [ -n "$EMAIL_IMAP_USER" ]; then
    CHANNELS_JSON+=", \"imapHost\": \"${EMAIL_IMAP_HOST}\", \"imapPort\": ${EMAIL_IMAP_PORT}"
    CHANNELS_JSON+=", \"imapUser\": \"${EMAIL_IMAP_USER}\", \"imapPassword\": \"${EMAIL_IMAP_PASSWORD}\""
fi
if [ -n "$EMAIL_SMTP_USER" ]; then
    CHANNELS_JSON+=", \"smtpHost\": \"${EMAIL_SMTP_HOST}\", \"smtpPort\": ${EMAIL_SMTP_PORT}"
    CHANNELS_JSON+=", \"smtpUser\": \"${EMAIL_SMTP_USER}\", \"smtpPassword\": \"${EMAIL_SMTP_PASSWORD}\""
fi
CHANNELS_JSON+="}"

# Telegram
CHANNELS_JSON+=", \"telegram\": {\"enabled\": ${TELEGRAM_ENABLED}"
if [ -n "$TELEGRAM_BOT_TOKEN" ]; then
    CHANNELS_JSON+=", \"botToken\": \"${TELEGRAM_BOT_TOKEN}\""
fi
CHANNELS_JSON+="}"

# Discord
CHANNELS_JSON+=", \"discord\": {\"enabled\": ${DISCORD_ENABLED}"
if [ -n "$DISCORD_BOT_TOKEN" ]; then
    CHANNELS_JSON+=", \"botToken\": \"${DISCORD_BOT_TOKEN}\""
fi
CHANNELS_JSON+="}"

# WhatsApp
CHANNELS_JSON+=", \"whatsapp\": {\"enabled\": ${WHATSAPP_ENABLED}}"

# Slack
CHANNELS_JSON+=", \"slack\": {\"enabled\": ${SLACK_ENABLED}"
if [ -n "$SLACK_BOT_TOKEN" ]; then
    CHANNELS_JSON+=", \"botToken\": \"${SLACK_BOT_TOKEN}\", \"appToken\": \"${SLACK_APP_TOKEN}\""
fi
CHANNELS_JSON+="}"
CHANNELS_JSON+="}"

cat > "$NANOBOT_CONFIG" << EOF
{
  "providers": {
    "${LLM_PROVIDER}": {
      "apiKey": "${LLM_API_KEY}",
      "apiBase": "${LLM_API_BASE}"
    }
  },
  "agents": {
    "defaults": {
      "model": "${LLM_MODEL}",
      "temperature": 0.3,
      "maxTokens": 8192,
      "memoryWindow": 50
    }
  },
  "channels": ${CHANNELS_JSON},
  "tools": {
    "restrictToWorkspace": false
  }
}
EOF
info "Nanobot config written to: $NANOBOT_CONFIG"

# ==================== 6. Link Skills ====================
info "[6/7] Linking Skills to Nanobot..."
rm -rf "$HOME/.nanobot/workspace/skills"
rm -f "$HOME/.nanobot/workspace/SOUL.md"
mkdir -p "$HOME/.nanobot/workspace"
cp -r "$DEPLOY_DIR/finagent/skills/" "$HOME/.nanobot/workspace/skills/"
cp "$DEPLOY_DIR/docs/SOUL.md" "$HOME/.nanobot/workspace/SOUL.md"
info "Skills linked"

# ==================== 7. Configure systemd Service ====================
info "[7/7] Configuring systemd service..."
SERVICE_FILE="/etc/systemd/system/finagent.service"

sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=FinAgent - A-Share AI Research Assistant
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=${DEPLOY_DIR}
ExecStartPre=${DEPLOY_DIR}/scripts/notify-start.sh
ExecStart=/bin/bash -c 'set -a; source ${DEPLOY_DIR}/.env; set +a; ${VENV_DIR}/bin/nanobot gateway'
Restart=always
RestartSec=10
Environment=PATH=${VENV_DIR}/bin:/usr/local/bin:/usr/bin
EnvironmentFile=${DEPLOY_DIR}/.env

# Logging
StandardOutput=journal
StandardError=journal
SyslogIdentifier=finagent

[Install]
WantedBy=multi-user.target
EOF

# Create startup notification script
cat > "${DEPLOY_DIR}/scripts/notify-start.sh" << 'NOTIFY_EOF'
#!/bin/bash
# Sends a Feishu notification when the service starts
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "$0")" && pwd)"
DEPLOY_DIR="$(dirname "$SCRIPT_DIR")"

# Load .env
if [ -f "$DEPLOY_DIR/.env" ]; then
    set -a
    source "$DEPLOY_DIR/.env"
    set +a
fi

FEISHU_CHAT_ID="${FEISHU_CHAT_ID:-}"
FEISHU_WEBHOOK_URL="${FEISHU_WEBHOOK_URL:-}"
FEISHU_APP_ID="${FEISHU_APP_ID:-}"
FEISHU_APP_SECRET="${FEISHU_APP_SECRET:-}"

hostname="$(hostname)"
notify_msg="**FinAgent Started** ✅\n\nHost: \`${hostname}\`\nTime: $(date '+%Y-%m-%d %H:%M:%S')"

send_notify() {
    # Method 1: Webhook
    if [ -n "$FEISHU_WEBHOOK_URL" ]; then
        local payload
        payload=$(printf '{"msg_type":"interactive","card":{"header":{"title":{"tag":"plain_text","content":"FinAgent Started ✅"}},"elements":[{"tag":"markdown","content":"%s"}]}}' "$notify_msg")
        curl -s --max-time 10 -X POST "$FEISHU_WEBHOOK_URL" \
            -H "Content-Type: application/json" \
            -d "$payload" > /dev/null 2>&1
        return
    fi

    # Method 2: Open API
    if [ -n "$FEISHU_APP_ID" ] && [ -n "$FEISHU_APP_SECRET" ] && [ -n "$FEISHU_CHAT_ID" ]; then
        local token_response token
        token_response=$(curl -s --max-time 10 -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
            -H "Content-Type: application/json" \
            -d "{\"app_id\":\"$FEISHU_APP_ID\",\"app_secret\":\"$FEISHU_APP_SECRET\"}" 2>/dev/null) || return 0

        token=$(echo "$token_response" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tenant_access_token',''))" 2>/dev/null) || return 0
        [ -z "$token" ] && return 0

        local card_body
        card_body=$(printf '{"msg_type":"interactive","card":{"header":{"title":{"tag":"plain_text","content":"FinAgent Started ✅"}},"elements":[{"tag":"markdown","content":"%s"}]}}' "$notify_msg")

        curl -s --max-time 10 -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
            -H "Authorization: Bearer $token" \
            -H "Content-Type: application/json" \
            -d "{\"receive_id\":\"$FEISHU_CHAT_ID\",$(echo "$card_body" | python3 -c "import sys; d=sys.stdin.read(); print(d[d.index(',')+1:])" 2>/dev/null)}" > /dev/null 2>&1 || true
    fi
}

send_notify
exit 0  # Never block service startup
NOTIFY_EOF
chmod +x "${DEPLOY_DIR}/scripts/notify-start.sh"

sudo systemctl daemon-reload
sudo systemctl enable finagent
info "systemd service configured"

# ==================== Start Service ====================
echo ""
info "=== Deployment Complete ==="
echo ""
echo "Start service:  sudo systemctl start finagent"
echo "Check status:   sudo systemctl status finagent"
echo "View logs:      sudo journalctl -u finagent -f"
echo "Stop service:   sudo systemctl stop finagent"
echo ""

# Check if API Key is configured
if [ -z "$LLM_API_KEY" ]; then
    warn "LLM_API_KEY is not set!"
    warn "Please edit $DEPLOY_DIR/.env and fill in your API Key"
    warn "Then run: sudo systemctl start finagent"
else
    info "Starting service..."
    sudo systemctl start finagent
    sleep 2
    sudo systemctl status finagent --no-pager -l
fi

echo ""

# ==================== Feishu Deployment Notification ====================
send_feishu_notification() {
    local hostname
    hostname="$(hostname)"
    local notify_msg
    notify_msg="**FinAgent Deployed** ✅\n\nHost: \`${hostname}\`\nTime: $(date '+%Y-%m-%d %H:%M:%S')\nStatus: Running"

    # Method 1: Webhook (simplest)
    if [ -n "$FEISHU_WEBHOOK_URL" ]; then
        local payload
        payload=$(printf '{"msg_type":"interactive","card":{"header":{"title":{"tag":"plain_text","content":"FinAgent Deployed ✅"}},"elements":[{"tag":"markdown","content":"%s"}]}}' "$notify_msg")
        curl -s -X POST "$FEISHU_WEBHOOK_URL" \
            -H "Content-Type: application/json" \
            -d "$payload" > /dev/null 2>&1 && \
            info "Feishu notification sent via webhook" || \
            warn "Failed to send Feishu webhook notification"
        return
    fi

    # Method 2: Feishu Open API (using app_id/app_secret + chat_id)
    if [ -n "$FEISHU_APP_ID" ] && [ -n "$FEISHU_APP_SECRET" ] && [ -n "$FEISHU_CHAT_ID" ]; then
        # Get tenant_access_token
        local token_response
        token_response=$(curl -s -X POST "https://open.feishu.cn/open-apis/auth/v3/tenant_access_token/internal" \
            -H "Content-Type: application/json" \
            -d "{\"app_id\":\"$FEISHU_APP_ID\",\"app_secret\":\"$FEISHU_APP_SECRET\"}" 2>/dev/null)

        local token
        token=$(echo "$token_response" | python3 -c "import sys,json; print(json.load(sys.stdin).get('tenant_access_token',''))" 2>/dev/null)

        if [ -n "$token" ]; then
            local card_body
            card_body=$(printf '{"msg_type":"interactive","card":{"header":{"title":{"tag":"plain_text","content":"FinAgent Deployed ✅"}},"elements":[{"tag":"markdown","content":"%s"}]}}' "$notify_msg")

            local send_response
            send_response=$(curl -s -X POST "https://open.feishu.cn/open-apis/im/v1/messages?receive_id_type=chat_id" \
                -H "Authorization: Bearer $token" \
                -H "Content-Type: application/json" \
                -d "{\"receive_id\":\"$FEISHU_CHAT_ID\",$(echo "$card_body" | python3 -c "import sys; d=sys.stdin.read(); print(d[d.index(',')+1:])" 2>/dev/null)}" 2>/dev/null)

            local send_code
            send_code=$(echo "$send_response" | python3 -c "import sys,json; print(json.load(sys.stdin).get('code',-1))" 2>/dev/null)

            if [ "$send_code" = "0" ]; then
                info "Feishu notification sent via Open API"
            else
                warn "Feishu API returned code=$send_response"
            fi
        else
            warn "Failed to get Feishu tenant_access_token"
        fi
        return
    fi

    # No notification configured
    if [ -n "$FEISHU_APP_ID" ] && [ -z "$FEISHU_CHAT_ID" ]; then
        warn "FEISHU_CHAT_ID not set — no startup notification will be sent"
        warn "Add FEISHU_CHAT_ID to .env to receive a message when the bot starts"
    fi
}

send_feishu_notification

echo ""
info "CLI test command: $VENV_DIR/bin/nanobot agent -m 'Check 600519'"
