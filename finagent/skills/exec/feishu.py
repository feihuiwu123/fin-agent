"""飞书消息收发 | Feishu Bot Messaging"""

from nanobot.agent.tools import tool
import logging

logger = logging.getLogger(__name__)


@tool
async def skill_feishu_send(chat_id: str, message: str, card: dict | None = None) -> bool:
    """
    通过飞书 Bot 发送消息或交互卡片。
    Send a message or interactive card via Feishu Bot.

    Args:
        chat_id: 飞书会话 ID | Feishu chat ID
        message: 文本消息 | Text message
        card: 交互卡片 JSON（可选）| Interactive card JSON (optional)
    Returns:
        发送是否成功 | Whether the send succeeded
    """
    # 骨架实现：记录日志，待飞书接入后替换为实际 API 调用
    # Skeleton: log the message, replace with actual Feishu API call when connected
    logger.info(f"[Feishu] Sending to {chat_id}: {message[:100]}...")
    if card:
        logger.info(f"[Feishu] Card: {str(card)[:100]}...")

    # TODO: 接入飞书 Open API
    # 1. 获取 tenant_access_token
    # 2. 调用 POST /im/v1/messages
    # 3. 处理返回结果
    return True
