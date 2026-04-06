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

# ==================== 配置区（部署前修改） ====================
# LLM 提供商: deepseek / qwen / openai
LLM_PROVIDER="${LLM_PROVIDER:-deepseek}"
LLM_API_KEY="${LLM_API_KEY:-}"
LLM_API_BASE="${LLM_API_BASE:-https://api.deepseek.com/v1}"
LLM_MODEL="${LLM_MODEL:-deepseek/deepseek-chat}"

# 飞书配置（可选，留空则不启用）
FEISHU_ENABLED="${FEISHU_ENABLED:-false}"
FEISHU_APP_ID="${FEISHU_APP_ID:-}"
FEISHU_APP_SECRET="${FEISHU_APP_SECRET:-}"

# 部署路径
DEPLOY_DIR="${DEPLOY_DIR:-$HOME/finagent}"
VENV_DIR="${DEPLOY_DIR}/.venv"

# ==================== 前置检查 ====================
info "=== FinAgent 部署脚本 ==="
info "部署目录: $DEPLOY_DIR"

# 检查是否 root
if [ "$(id -u)" -eq 0 ]; then
    error "请不要使用 root 运行此脚本，使用普通用户即可"
fi

# 检查系统
if ! command -v apt &>/dev/null; then
    warn "非 Debian/Ubuntu 系统，可能需要手动安装依赖"
fi

# ==================== 1. 安装系统依赖 ====================
info "[1/7] 安装系统依赖..."
sudo apt update -qq
sudo apt install -y python3.11 python3.11-venv python3-pip git curl 2>/dev/null || {
    warn "python3.11 安装失败，尝试 python3.12..."
    sudo apt install -y python3.12 python3.12-venv python3-pip git curl 2>/dev/null || {
        error "Python 3.11+ 安装失败，请手动安装"
    }
    PYTHON="python3.12"
}
PYTHON="${PYTHON:-python3.11}"
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
  "channels": {
    "feishu": {
      "enabled": ${FEISHU_ENABLED},
      "appId": "${FEISHU_APP_ID}",
      "appSecret": "${FEISHU_APP_SECRET}"
    }
  },
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
ExecStart=${VENV_DIR}/bin/nanobot gateway
Restart=always
RestartSec=10
Environment=PATH=${VENV_DIR}/bin:/usr/local/bin:/usr/bin
Environment=FINAGENT_DB_PATH=${DEPLOY_DIR}/finagent.db

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
    warn "请编辑 $NANOBOT_CONFIG 填入你的 API Key"
    warn "然后运行: sudo systemctl start finagent"
else
    info "正在启动服务..."
    sudo systemctl start finagent
    sleep 2
    sudo systemctl status finagent --no-pager -l
fi

echo ""
info "CLI 测试命令: $VENV_DIR/bin/nanobot agent -m '查 600519'"
