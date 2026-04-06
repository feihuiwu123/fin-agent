"""Tests for risk control engine"""

from finagent.skills.exec.risk_check import (
    check_position_limit,
    check_daily_loss,
    MAX_SINGLE_POSITION_PCT,
    MAX_DAILY_LOSS_PCT,
)


class TestRiskCheck:
    def test_position_limit_pass(self):
        assert check_position_limit("600519", 10000, 100000) is True

    def test_position_limit_exceed(self):
        assert check_position_limit("600519", 25000, 100000) is False

    def test_position_limit_exact_boundary(self):
        assert check_position_limit("600519", 20000, 100000) is True

    def test_daily_loss_pass(self):
        assert check_daily_loss(-2000, 100000) is True

    def test_daily_loss_exceed(self):
        assert check_daily_loss(-5000, 100000) is False

    def test_daily_loss_exact_boundary(self):
        assert check_daily_loss(-3000, 100000) is True

    def test_constants(self):
        assert MAX_SINGLE_POSITION_PCT == 0.20
        assert MAX_DAILY_LOSS_PCT == 0.03
