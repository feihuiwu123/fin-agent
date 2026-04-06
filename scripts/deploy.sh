#!/bin/bash
# FinAgent 一键部署脚本 | FinAgent One-Click Deploy Script
# 用法: bash deploy.sh
# 系统要求: Ubuntu 22.04+ / Debian 12+

set -euo pipefail

# ==================== 颜色输出 ====================
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
NC='\033[0m'

info()  { echo -e "${GREEN}[INFO]${NC} $1"; }
warn()  { echo -e "${YELLOW}[WARN]${NC} $1"; }
error() { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# ==================== 配置区（从 .env 读取） ====================
# LLM 提供商: deepseek / opencode / minimax / qwen / openrouter
LLM_PROVIDER="${LLM_PROVIDER:-deepseek}"
LLM_API_KEY="${LLM_API_KEY:-}"
LLM_API_BASE="${LLM_API_BASE:-}"
LLM_MODEL="${LLM_MODEL:-}"

# 根据提供商自动设置默认值
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

# 渠道配置（可选，留空则不启用）
FEISHU_ENABLED="${FEISHU_ENABLED:-false}"
FEISHU_APP_ID="${FEISHU_APP_ID:-}"
FEISHU_APP_SECRET="${FEISHU_APP_SECRET:-}"
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

# 部署路径
DEPLOY_DIR="${DEPLOY_DIR:-$HOME/finagent}"
VENV_DIR="${DEPLOY_DIR}/.venv"

# ==================== 前置检查 ====================
info "=== FinAgent 部署脚本 ==="
info "部署目录: $DEPLOY_DIR"

# 加载 .env 环境变量
if [ -f "$DEPLOY_DIR/.env" ]; then
    info "加载 .env 环境变量..."
    set -a
    source "$DEPLOY_DIR/.env"
    set +a
elif [ -f ".env" ]; then
    info "加载 .env 环境变量..."
    set -a
    source ".env"
    set +a
else
    warn ".env 文件不存在，将使用环境变量或默认值"
fi

# 安全检查：禁止 root 运行
if [ "$(id -u)" -eq 0 ]; then
    error "禁止使用 root 运行此脚本！请创建普通用户后部署\n  示例: useradd -m finagent && su - finagent"
fi

# 检查系统
if ! command -v apt &>/dev/null; then
    warn "非 Debian/Ubuntu 系统，可能需要手动安装依赖"
fi

# ==================== 1. 安装系统依赖 ====================
info "[1/7] 安装系统依赖..."

# 优先检测系统已有 Python 3.11+
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
        info "尝试安装 python3.${ver}..."
        sudo apt install -y python3.${ver} python3.${ver}-venv python3-pip git curl 2>/dev/null && {
            PYTHON="python3.${ver}"
            break
        }
    done
    if [ -z "$PYTHON" ]; then
        error "Python 3.11+ 安装失败，请手动安装"
    fi
fi

info "Python 版本: $($PYTHON --version)"

# ==================== 2. 克隆/更新代码 ====================
info "[2/7] 准备代码..."
if [ -d "$DEPLOY_DIR/.git" ]; then
    cd "$DEPLOY_DIR"
    git pull
    info "代码已更新"
else
    mkdir -p "$(dirname "$DEPLOY_DIR")"
    # 如果有 git 仓库，取消下面这行的注释并修改 URL
    # git clone https://github.com/yourname/finagent.git "$DEPLOY_DIR"
    info "请将代码复制到 $DEPLOY_DIR，或修改脚本中的 git clone 地址"
fi
cd "$DEPLOY_DIR"

# ==================== 3. 创建虚拟环境 ====================
info "[3/7] 创建 Python 虚拟环境..."
$PYTHON -m venv "$VENV_DIR"
source "$VENV_DIR/bin/activate"
pip install --upgrade pip -q

# ==================== 4. 安装 Python 依赖 ====================
info "[4/7] 安装 Python 依赖..."
pip install -e ".[dev]" -q
pip install nanobot-ai -q
info "依赖安装完成"

# ==================== 5. 初始化 Nanobot 配置 ====================
info "[5/7] 初始化 Nanobot 配置..."
NANOBOT_CONFIG="$HOME/.nanobot/config.json"
mkdir -p "$HOME/.nanobot"

# 构建 channels JSON
CHANNELS_JSON="{"

# 飞书
CHANNELS_JSON+="\"feishu\": {\"enabled\": ${FEISHU_ENABLED}"
if [ -n "$FEISHU_APP_ID" ]; then
    CHANNELS_JSON+=", \"appId\": \"${FEISHU_APP_ID}\", \"appSecret\": \"${FEISHU_APP_SECRET}\""
fi
CHANNELS_JSON+="}"

# 微信
CHANNELS_JSON+=", \"weixin\": {\"enabled\": ${WECHAT_ENABLED}}"

# 钉钉
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
info "Nanobot 配置已写入: $NANOBOT_CONFIG"

# ==================== 6. 链接 Skills ====================
info "[6/7] 链接 Skills 到 Nanobot..."
rm -rf "$HOME/.nanobot/workspace/skills"
rm -f "$HOME/.nanobot/workspace/SOUL.md"
mkdir -p "$HOME/.nanobot/workspace"
cp -r "$DEPLOY_DIR/finagent/skills/" "$HOME/.nanobot/workspace/skills/"
cp "$DEPLOY_DIR/docs/SOUL.md" "$HOME/.nanobot/workspace/SOUL.md"
info "Skills 已链接"

# ==================== 7. 配置 systemd 服务 ====================
info "[7/7] 配置 systemd 服务..."
SERVICE_FILE="/etc/systemd/system/finagent.service"

sudo tee "$SERVICE_FILE" > /dev/null << EOF
[Unit]
Description=FinAgent - A-Share AI Research Assistant
After=network.target

[Service]
Type=simple
User=$(whoami)
WorkingDirectory=${DEPLOY_DIR}
ExecStart=/bin/bash -c 'set -a; source ${DEPLOY_DIR}/.env; set +a; ${VENV_DIR}/bin/nanobot gateway'
Restart=always
RestartSec=10
Environment=PATH=${VENV_DIR}/bin:/usr/local/bin:/usr/bin
EnvironmentFile=${DEPLOY_DIR}/.env

# 日志
StandardOutput=journal
StandardError=journal
SyslogIdentifier=finagent

[Install]
WantedBy=multi-user.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable finagent
info "systemd 服务已配置"

# ==================== 启动服务 ====================
echo ""
info "=== 部署完成 ==="
echo ""
echo "启动服务: sudo systemctl start finagent"
echo "查看状态: sudo systemctl status finagent"
echo "查看日志: sudo journalctl -u finagent -f"
echo "停止服务: sudo systemctl stop finagent"
echo ""

# 检查 API Key 是否配置
if [ -z "$LLM_API_KEY" ]; then
    warn "LLM_API_KEY 未设置！"
    warn "请编辑 $DEPLOY_DIR/.env 填入你的 API Key"
    warn "然后运行: sudo systemctl start finagent"
else
    info "正在启动服务..."
    sudo systemctl start finagent
    sleep 2
    sudo systemctl status finagent --no-pager -l
fi

echo ""
info "CLI 测试命令: $VENV_DIR/bin/nanobot agent -m '查 600519'"
