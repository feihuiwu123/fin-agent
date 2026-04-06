"""Tests for database layer"""

import os
import tempfile
import pytest

from finagent.db.database import (
    position_add,
    position_list,
    position_delete,
    position_update,
    alert_add,
    alert_list,
    alert_deactivate,
    trade_log_add,
    trade_log_list,
)


@pytest.fixture(autouse=True)
def use_temp_db(monkeypatch):
    tmp = tempfile.NamedTemporaryFile(suffix=".db", delete=False)
    tmp.close()
    monkeypatch.setenv("FINAGENT_DB_PATH", tmp.name)
    yield tmp.name
    if os.path.exists(tmp.name):
        os.unlink(tmp.name)


class TestPositions:
    def test_add_and_list(self):
        p = position_add("600519", 1750.0, 100)
        assert p.symbol == "600519"
        assert p.cost == 1750.0
        assert p.qty == 100

        positions = position_list()
        assert len(positions) == 1
        assert positions[0].symbol == "600519"

    def test_delete(self):
        p = position_add("000001", 15.0, 200)
        assert position_delete(p.id)
        assert len(position_list()) == 0

    def test_update(self):
        p = position_add("300750", 200.0, 50)
        updated = position_update(p.id, cost=210.0)
        assert updated is not None
        assert updated.cost == 210.0


class TestAlerts:
    def test_add_and_list(self):
        alert = alert_add("600519", "跌破1700", "price_below", 1700.0)
        assert alert.symbol == "600519"
        assert alert.target_price == 1700.0

        alerts = alert_list()
        assert len(alerts) == 1

    def test_deactivate(self):
        alert = alert_add("000001", "突破16", "price_above", 16.0)
        assert alert_deactivate(alert.id)
        assert len(alert_list(active_only=True)) == 0
        assert len(alert_list(active_only=False)) == 1


class TestTradeLog:
    def test_add_and_list(self):
        trade_log_add("600519", "buy", 1750.0, 100, "test")
        logs = trade_log_list()
        assert len(logs) == 1
        assert logs[0].symbol == "600519"

    def test_filter_by_symbol(self):
        trade_log_add("600519", "buy", 1750.0, 100)
        trade_log_add("000001", "sell", 15.0, 200)
        logs = trade_log_list(symbol="600519")
        assert len(logs) == 1
        assert logs[0].symbol == "600519"
