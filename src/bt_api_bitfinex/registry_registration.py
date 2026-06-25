"""Bitfinex registry registration."""

from bt_api_base.plugins.protocol import PluginInfo
from bt_api_base.registry import ExchangeRegistry

from bt_api_bitfinex.exchange_data import BitfinexExchangeDataSpot
from bt_api_bitfinex.feeds.live_bitfinex import BitfinexRequestDataSpot
from bt_api_bitfinex.plugin import BITFINEX_PLUGIN_INFO


def register_bitfinex(
    registry: ExchangeRegistry | type[ExchangeRegistry] | None = None,
) -> PluginInfo:
    """Register Bitfinex plugin with ExchangeRegistry."""
    if registry is None:
        registry = ExchangeRegistry
    registry.register_feed("BITFINEX___SPOT", BitfinexRequestDataSpot)
    registry.register_exchange_data("BITFINEX___SPOT", BitfinexExchangeDataSpot)
    return BITFINEX_PLUGIN_INFO
