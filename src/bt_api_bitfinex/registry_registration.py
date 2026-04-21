"""Bitfinex registry registration."""

from bt_api_base.registry import ExchangeRegistry

from bt_api_bitfinex.feeds.live_bitfinex import BitfinexRequestDataSpot
from bt_api_bitfinex.exchange_data import BitfinexExchangeDataSpot


def register_bitfinex(registry: ExchangeRegistry | None = None) -> None:
    """Register Bitfinex plugin with ExchangeRegistry."""
    if registry is None:
        registry = ExchangeRegistry()
    registry.register_feed("BITFINEX___SPOT", BitfinexRequestDataSpot)
    registry.register_exchange_data("BITFINEX___SPOT", BitfinexExchangeDataSpot)
