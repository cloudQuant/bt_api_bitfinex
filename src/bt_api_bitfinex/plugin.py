"""Bitfinex plugin registration."""

from __future__ import annotations

from typing import Any

from bt_api_base.plugins.protocol import PluginInfo

from bt_api_bitfinex.exchange_data import BitfinexExchangeDataSpot
from bt_api_bitfinex.feeds.live_bitfinex import BitfinexRequestDataSpot

BITFINEX_PLUGIN_INFO = PluginInfo(
    name="bt_api_bitfinex",
    version="0.1.1",
    core_requires=">=0.15,<1.0",
    supported_exchanges=("BITFINEX___SPOT",),
    supported_asset_types=("SPOT",),
)


def register_plugin(registry: Any, runtime_factory: Any | None = None) -> PluginInfo:
    registry.register_feed("BITFINEX___SPOT", BitfinexRequestDataSpot)
    registry.register_exchange_data("BITFINEX___SPOT", BitfinexExchangeDataSpot)
    return BITFINEX_PLUGIN_INFO
