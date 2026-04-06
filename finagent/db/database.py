"""SQLite 数据库操作 | SQLite Database Operations"""

import sqlite3
import os
from datetime import datetime
from typing import Optional
from pathlib import Path

from .models import Position, Alert, TradeLog

DB_PATH = os.environ.get("FINAGENT_DB_PATH", str(Path.home() / ".finagent" / "finagent.db"))


def _get_connection(db_path: str = DB_PATH) -> sqlite3.Connection:
    """获取数据库连接 | Get database connection"""
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.row_factory = sqlite3.Row
    return conn


def init_db(db_path: str = DB_PATH) -> None:
    """初始化数据库表 | Initialize database tables"""
    conn = _get_connection(db_path)
    conn.executescript("""
        CREATE TABLE IF NOT EXISTS positions (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            name TEXT DEFAULT '',
            cost REAL NOT NULL,
            qty INTEGER NOT NULL,
            added_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
        );

        CREATE TABLE IF NOT EXISTS alerts (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            condition TEXT NOT NULL,
            condition_type TEXT NOT NULL,
            target_price REAL,
            active INTEGER DEFAULT 1,
            created_at TEXT NOT NULL,
            triggered_at TEXT
        );

        CREATE TABLE IF NOT EXISTS trade_log (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            symbol TEXT NOT NULL,
            side TEXT NOT NULL,
            price REAL NOT NULL,
            qty INTEGER NOT NULL,
            reason TEXT DEFAULT '',
            created_at TEXT NOT NULL
        );
    """)
    conn.commit()
    conn.close()


def position_add(symbol: str, cost: float, qty: int, name: str = "") -> Position:
    """添加持仓 | Add a position"""
    init_db()
    conn = _get_connection()
    now = datetime.now().isoformat()
    cursor = conn.execute(
        "INSERT INTO positions (symbol, name, cost, qty, added_at, updated_at) VALUES (?, ?, ?, ?, ?, ?)",
        (symbol, name, cost, qty, now, now),
    )
    conn.commit()
    position = Position(
        id=cursor.lastrowid,
        symbol=symbol,
        name=name,
        cost=cost,
        qty=qty,
        added_at=now,
        updated_at=now,
    )
    conn.close()
    return position


def position_list() -> list[Position]:
    """获取全部持仓 | List all positions"""
    init_db()
    conn = _get_connection()
    rows = conn.execute("SELECT * FROM positions ORDER BY added_at DESC").fetchall()
    positions = [
        Position(
            id=row["id"],
            symbol=row["symbol"],
            name=row["name"],
            cost=row["cost"],
            qty=row["qty"],
            added_at=row["added_at"],
            updated_at=row["updated_at"],
        )
        for row in rows
    ]
    conn.close()
    return positions


def position_delete(position_id: int) -> bool:
    """删除持仓 | Delete a position"""
    init_db()
    conn = _get_connection()
    cursor = conn.execute("DELETE FROM positions WHERE id = ?", (position_id,))
    conn.commit()
    deleted = cursor.rowcount > 0
    conn.close()
    return deleted


def position_update(
    position_id: int, cost: Optional[float] = None, qty: Optional[int] = None
) -> Optional[Position]:
    """更新持仓 | Update a position"""
    init_db()
    conn = _get_connection()
    now = datetime.now().isoformat()
    updates = []
    params: list = []
    if cost is not None:
        updates.append("cost = ?")
        params.append(cost)
    if qty is not None:
        updates.append("qty = ?")
        params.append(qty)
    updates.append("updated_at = ?")
    params.append(now)
    params.append(position_id)

    conn.execute(f"UPDATE positions SET {', '.join(updates)} WHERE id = ?", params)
    conn.commit()

    row = conn.execute("SELECT * FROM positions WHERE id = ?", (position_id,)).fetchone()
    conn.close()
    if row is None:
        return None
    return Position(
        id=row["id"],
        symbol=row["symbol"],
        name=row["name"],
        cost=row["cost"],
        qty=row["qty"],
        added_at=row["added_at"],
        updated_at=row["updated_at"],
    )


def alert_add(
    symbol: str, condition: str, condition_type: str, target_price: Optional[float] = None
) -> Alert:
    """添加预警 | Add an alert"""
    init_db()
    conn = _get_connection()
    now = datetime.now().isoformat()
    cursor = conn.execute(
        "INSERT INTO alerts (symbol, condition, condition_type, target_price, active, created_at) VALUES (?, ?, ?, ?, 1, ?)",
        (symbol, condition, condition_type, target_price, now),
    )
    conn.commit()
    alert = Alert(
        id=cursor.lastrowid,
        symbol=symbol,
        condition=condition,
        condition_type=condition_type,
        target_price=target_price,
        active=True,
        created_at=now,
    )
    conn.close()
    return alert


def alert_list(active_only: bool = True) -> list[Alert]:
    """获取预警列表 | List alerts"""
    init_db()
    conn = _get_connection()
    query = (
        "SELECT * FROM alerts WHERE active = 1 ORDER BY created_at DESC"
        if active_only
        else "SELECT * FROM alerts ORDER BY created_at DESC"
    )
    rows = conn.execute(query).fetchall()
    alerts = [
        Alert(
            id=row["id"],
            symbol=row["symbol"],
            condition=row["condition"],
            condition_type=row["condition_type"],
            target_price=row["target_price"],
            active=bool(row["active"]),
            created_at=row["created_at"],
            triggered_at=row["triggered_at"],
        )
        for row in rows
    ]
    conn.close()
    return alerts


def alert_deactivate(alert_id: int) -> bool:
    """停用预警 | Deactivate an alert"""
    init_db()
    conn = _get_connection()
    now = datetime.now().isoformat()
    conn.execute("UPDATE alerts SET active = 0, triggered_at = ? WHERE id = ?", (now, alert_id))
    conn.commit()
    deactivated = conn.total_changes > 0
    conn.close()
    return deactivated


def trade_log_add(symbol: str, side: str, price: float, qty: int, reason: str = "") -> TradeLog:
    """记录交易日志 | Add a trade log entry"""
    init_db()
    conn = _get_connection()
    now = datetime.now().isoformat()
    cursor = conn.execute(
        "INSERT INTO trade_log (symbol, side, price, qty, reason, created_at) VALUES (?, ?, ?, ?, ?, ?)",
        (symbol, side, price, qty, reason, now),
    )
    conn.commit()
    log = TradeLog(
        id=cursor.lastrowid,
        symbol=symbol,
        side=side,
        price=price,
        qty=qty,
        reason=reason,
        created_at=now,
    )
    conn.close()
    return log


def trade_log_list(symbol: Optional[str] = None, limit: int = 50) -> list[TradeLog]:
    """获取交易日志 | List trade logs"""
    init_db()
    conn = _get_connection()
    if symbol:
        rows = conn.execute(
            "SELECT * FROM trade_log WHERE symbol = ? ORDER BY created_at DESC LIMIT ?",
            (symbol, limit),
        ).fetchall()
    else:
        rows = conn.execute(
            "SELECT * FROM trade_log ORDER BY created_at DESC LIMIT ?", (limit,)
        ).fetchall()
    logs = [
        TradeLog(
            id=row["id"],
            symbol=row["symbol"],
            side=row["side"],
            price=row["price"],
            qty=row["qty"],
            reason=row["reason"],
            created_at=row["created_at"],
        )
        for row in rows
    ]
    conn.close()
    return logs
