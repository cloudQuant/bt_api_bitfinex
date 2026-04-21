"""Bitfinex plugin registration."""

from bt_api_base.plugins.protocol import PluginInfo

BITFINEX_PLUGIN_INFO = PluginInfo(
    name="bt_api_bitfinex",
    version="0.1.0",
    core_requires=">=0.15,<1.0",
    supported_exchanges=("BITFINEX___SPOT",),
    supported_asset_types=("SPOT",),
)
