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
