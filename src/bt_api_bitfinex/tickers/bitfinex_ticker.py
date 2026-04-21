"""Bitfinex Ticker Data Container."""

from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.tickers.ticker import TickerData
from bt_api_base.functions.utils import from_dict_get_float, from_dict_get_string


class BitfinexTickerData(TickerData):
    """Bitfinex ticker data container."""

    def __init__(
        self,
        ticker_info: str | dict[str, Any],
        symbol_name: str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(ticker_info, has_been_json_encoded)
        self.exchange_name = "BITFINEX"
        self.local_update_time = time.time()
        self.ticker_data: dict[str, Any] | list[Any] | None = (
            ticker_info if has_been_json_encoded and isinstance(ticker_info, (dict, list)) else None
        )
        self.ticker_symbol_name: str | None = None
        self.has_been_init_data = False
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.server_time: float | None = None
        self.bid_price: float | None = None
        self.ask_price: float | None = None
        self.bid_volume: float | None = None
        self.ask_volume: float | None = None
        self.last_price: float | None = None
        self.daily_change: float | None = None
        self.daily_change_percentage: float | None = None
        self.volume: float | None = None
        self.high: float | None = None
        self.low: float | None = None
        self.all_data: dict[str, Any] | None = None

    def init_data(self) -> BitfinexTickerData:
        if not self.has_been_json_encoded:
            self.ticker_data = json.loads(self.ticker_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.ticker_data, list) and len(self.ticker_data) >= 8:
            self.ticker_symbol_name = from_dict_get_string(self.ticker_data[0], "")
            self.bid_price = from_dict_get_float(self.ticker_data[1], 0.0)
            self.bid_volume = from_dict_get_float(self.ticker_data[2], 0.0)
            self.ask_price = from_dict_get_float(self.ticker_data[3], 0.0)
            self.ask_volume = from_dict_get_float(self.ticker_data[4], 0.0)
            self.daily_change = from_dict_get_float(self.ticker_data[5], 0.0)
            self.daily_change_percentage = from_dict_get_float(self.ticker_data[6], 0.0)
            self.last_price = from_dict_get_float(self.ticker_data[7], 0.0)
            self.volume = (
                from_dict_get_float(self.ticker_data[8], 0.0) if len(self.ticker_data) > 8 else None
            )
            self.high = (
                from_dict_get_float(self.ticker_data[9], 0.0) if len(self.ticker_data) > 9 else None
            )
            self.low = (
                from_dict_get_float(self.ticker_data[10], 0.0)
                if len(self.ticker_data) > 10
                else None
            )
            self.server_time = time.time()

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
                "ticker_symbol_name": self.ticker_symbol_name,
                "server_time": self.server_time,
                "bid_price": self.bid_price,
                "ask_price": self.ask_price,
                "bid_volume": self.bid_volume,
                "ask_volume": self.ask_volume,
                "last_price": self.last_price,
                "daily_change": self.daily_change,
                "daily_change_percentage": self.daily_change_percentage,
                "volume": self.volume,
                "high": self.high,
                "low": self.low,
            }
        return self.all_data or {}

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

    def get_ticker_symbol_name(self) -> str | None:
        return self.ticker_symbol_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_server_time(self) -> float | None:
        return self.server_time

    def get_bid_price(self) -> float | None:
        return self.bid_price

    def get_ask_price(self) -> float | None:
        return self.ask_price

    def get_bid_volume(self) -> float | None:
        return self.bid_volume

    def get_ask_volume(self) -> float | None:
        return self.ask_volume

    def get_last_price(self) -> float | None:
        return self.last_price

    def get_daily_change(self) -> float | None:
        return self.daily_change

    def get_daily_change_percentage(self) -> float | None:
        return self.daily_change_percentage

    def get_volume(self) -> float | None:
        return self.volume

    def get_high(self) -> float | None:
        return self.high

    def get_low(self) -> float | None:
        return self.low


class BitfinexWssTickerData(BitfinexTickerData):
    """Bitfinex WebSocket ticker data container."""

    def init_data(self) -> BitfinexWssTickerData:
        if not self.has_been_json_encoded:
            self.ticker_data = json.loads(self.ticker_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.ticker_data, list) and len(self.ticker_data) >= 12:
            self.ticker_symbol_name = self.ticker_data[0]
            self.bid_price = float(self.ticker_data[1])
            self.bid_volume = float(self.ticker_data[2])
            self.ask_price = float(self.ticker_data[3])
            self.ask_volume = float(self.ticker_data[4])
            self.daily_change = float(self.ticker_data[5])
            self.daily_change_percentage = float(self.ticker_data[6])
            self.last_price = float(self.ticker_data[7])
            self.volume = float(self.ticker_data[8]) if len(self.ticker_data) > 8 else None
            self.high = float(self.ticker_data[9]) if len(self.ticker_data) > 9 else None
            self.low = float(self.ticker_data[10]) if len(self.ticker_data) > 10 else None
            self.server_time = (
                float(self.ticker_data[11]) / 1000 if len(self.ticker_data) > 11 else time.time()
            )

        self.has_been_init_data = True
        return self


class BitfinexRequestTickerData(BitfinexTickerData):
    """Bitfinex REST API ticker data container."""

    def init_data(self) -> BitfinexRequestTickerData:
        if not self.has_been_json_encoded:
            self.ticker_data = json.loads(self.ticker_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.ticker_data, list) and len(self.ticker_data) >= 8:
            self.ticker_symbol_name = self.ticker_data[0]
            self.bid_price = float(self.ticker_data[1])
            self.bid_volume = float(self.ticker_data[2])
            self.ask_price = float(self.ticker_data[3])
            self.ask_volume = float(self.ticker_data[4])
            self.daily_change = float(self.ticker_data[5])
            self.daily_change_percentage = float(self.ticker_data[6])
            self.last_price = float(self.ticker_data[7])
            self.volume = float(self.ticker_data[8]) if len(self.ticker_data) > 8 else None
            self.high = float(self.ticker_data[9]) if len(self.ticker_data) > 9 else None
            self.low = float(self.ticker_data[10]) if len(self.ticker_data) > 10 else None
            self.server_time = time.time()

        self.has_been_init_data = True
        return self
