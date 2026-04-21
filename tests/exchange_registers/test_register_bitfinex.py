"""Tests for exchange_registers/register_bitfinex.py."""

from __future__ import annotations

from bt_api_bitfinex.registry_registration import register_bitfinex


class TestRegisterBitfinex:
    """Tests for Bitfinex registration module."""

    def test_module_imports(self):
        """Test module can be imported."""
        assert register_bitfinex is not None
