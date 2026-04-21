"""Tests for BitfinexExchangeData container."""

from __future__ import annotations

from bt_api_bitfinex.exchange_data import BitfinexExchangeData


class TestBitfinexExchangeData:
    """Tests for BitfinexExchangeData."""

    def test_init(self):
        """Test initialization."""
        exchange = BitfinexExchangeData()

        assert exchange.exchange_name == "BITFINEX"
