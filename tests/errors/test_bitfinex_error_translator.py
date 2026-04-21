"""Tests for BitfinexErrorTranslator."""

from __future__ import annotations

from bt_api_bitfinex.errors.bitfinex_translator import BitfinexErrorTranslator


class TestBitfinexErrorTranslator:
    """Tests for BitfinexErrorTranslator."""

    def test_error_map_exists(self):
        """Test ERROR_MAP is defined."""
        assert hasattr(BitfinexErrorTranslator, "ERROR_MAP")
