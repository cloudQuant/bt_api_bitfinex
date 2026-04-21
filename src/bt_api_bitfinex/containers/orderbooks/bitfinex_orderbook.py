"""Bitfinex OrderBook Data Container."""

from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.orderbooks.orderbook import OrderBookData


class BitfinexOrderBookData(OrderBookData):
    """Bitfinex orderbook data container."""

    def __init__(
        self,
        orderbook_info: str | dict,
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(orderbook_info, has_been_json_encoded)
        self.exchange_name = "BITFINEX"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.orderbook_info = orderbook_info
        self.orderbook_data: Any = orderbook_info if has_been_json_encoded else None
        self.bids: list[dict[str, Any]] = []
        self.asks: list[dict[str, Any]] = []
        self.timestamp: float | None = None
        self.all_data: dict[str, Any] | None = None
        self.has_been_init_data = False

    def init_data(self) -> BitfinexOrderBookData:
        if not self.has_been_json_encoded:
            if isinstance(self.orderbook_info, str):
                self.orderbook_data = json.loads(self.orderbook_info)
            else:
                self.orderbook_data = self.orderbook_info
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.orderbook_data, list):
            self.bids = []
            self.asks = []

            for level in self.orderbook_data:
                if len(level) >= 3:
                    price = float(level[0])
                    count = int(level[1])
                    amount = float(level[2])

                    if amount > 0:
                        self.bids.append(
                            {
                                "price": price,
                                "count": count,
                                "amount": amount,
                                "total": price * amount,
                            }
                        )
                    else:
                        self.asks.append(
                            {
                                "price": price,
                                "count": count,
                                "amount": abs(amount),
                                "total": price * abs(amount),
                            }
                        )

        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "bids": self.bids,
                "asks": self.asks,
                "timestamp": self.timestamp,
                "bid_count": len(self.bids),
                "ask_count": len(self.asks),
                "bid_volume": sum(bid["amount"] for bid in self.bids),
                "ask_volume": sum(ask["amount"] for ask in self.asks),
            }
        return self.all_data

    def __str__(self) -> str:
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_local_update_time(self) -> float:
        return self.local_update_time

    def get_symbol_name(self) -> str:
        return self.symbol_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_bids(self) -> list[dict[str, Any]]:
        if not self.has_been_init_data:
            self.init_data()
        return self.bids

    def get_asks(self) -> list[dict[str, Any]]:
        if not self.has_been_init_data:
            self.init_data()
        return self.asks

    def get_timestamp(self) -> float | None:
        return self.timestamp

    def get_bid_price(self, level: int = 0) -> float | None:
        if not self.has_been_init_data:
            self.init_data()
        if level < len(self.bids):
            return float(self.bids[level]["price"])
        return None

    def get_ask_price(self, level: int = 0) -> float | None:
        if not self.has_been_init_data:
            self.init_data()
        if level < len(self.asks):
            return float(self.asks[level]["price"])
        return None

    def get_bid_volume(self, level: int = 0) -> float | None:
        if not self.has_been_init_data:
            self.init_data()
        if level < len(self.bids):
            return float(self.bids[level]["amount"])
        return None

    def get_ask_volume(self, level: int = 0) -> float | None:
        if not self.has_been_init_data:
            self.init_data()
        if level < len(self.asks):
            return float(self.asks[level]["amount"])
        return None

    def get_bid_count(self, level: int = 0) -> int | None:
        if not self.has_been_init_data:
            self.init_data()
        if level < len(self.bids):
            return int(self.bids[level]["count"])
        return None

    def get_ask_count(self, level: int = 0) -> int | None:
        if not self.has_been_init_data:
            self.init_data()
        if level < len(self.asks):
            return int(self.asks[level]["count"])
        return None

    def get_spread(self) -> float | None:
        if not self.has_been_init_data:
            self.init_data()
        if self.bids and self.asks:
            return float(self.asks[0]["price"]) - float(self.bids[0]["price"])
        return None

    def get_mid_price(self) -> float | None:
        if not self.has_been_init_data:
            self.init_data()
        if self.bids and self.asks:
            return (float(self.bids[0]["price"]) + float(self.asks[0]["price"])) / 2
        return None

    def get_total_bid_volume(self) -> float:
        if not self.has_been_init_data:
            self.init_data()
        return sum(float(bid["amount"]) for bid in self.bids)

    def get_total_ask_volume(self) -> float:
        if not self.has_been_init_data:
            self.init_data()
        return sum(float(ask["amount"]) for ask in self.asks)

    def get_total_bid_value(self) -> float:
        if not self.has_been_init_data:
            self.init_data()
        return sum(float(bid["total"]) for bid in self.bids)

    def get_total_ask_value(self) -> float:
        if not self.has_been_init_data:
            self.init_data()
        return sum(float(ask["total"]) for ask in self.asks)

    def get_bid_levels(self, levels: int = 5) -> list[dict[str, Any]]:
        if not self.has_been_init_data:
            self.init_data()
        return self.bids[:levels]

    def get_ask_levels(self, levels: int = 5) -> list[dict[str, Any]]:
        if not self.has_been_init_data:
            self.init_data()
        return self.asks[:levels]

    def get_price_impact(self, volume_ratio: float = 0.1) -> dict[str, Any]:
        if not self.has_been_init_data:
            self.init_data()

        buy_impact = None
        if self.bids:
            total_volume = self.get_total_bid_volume()
            target_volume = total_volume * volume_ratio
            cumulative_volume = 0.0
            weighted_price = 0.0
            for bid in self.bids:
                cumulative_volume += bid["amount"]
                weighted_price += bid["price"] * bid["amount"]
                if cumulative_volume >= target_volume:
                    buy_impact = weighted_price / cumulative_volume
                    break

        sell_impact = None
        if self.asks:
            total_volume = self.get_total_ask_volume()
            target_volume = total_volume * volume_ratio
            cumulative_volume = 0.0
            weighted_price = 0.0
            for ask in self.asks:
                cumulative_volume += ask["amount"]
                weighted_price += ask["price"] * ask["amount"]
                if cumulative_volume >= target_volume:
                    sell_impact = weighted_price / cumulative_volume
                    break

        return {"buy_impact": buy_impact, "sell_impact": sell_impact, "spread": self.get_spread()}


class BitfinexWssOrderBookData(BitfinexOrderBookData):
    """Bitfinex WebSocket orderbook container."""


class BitfinexRequestOrderBookData(BitfinexOrderBookData):
    """Bitfinex REST API orderbook container."""
