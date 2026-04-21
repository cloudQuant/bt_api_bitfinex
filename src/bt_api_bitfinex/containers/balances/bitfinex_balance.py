"""Bitfinex Balance Data Container."""

from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.balances.balance import BalanceData


class BitfinexSpotRequestBalanceData(BalanceData):
    """Bitfinex Spot Request Balance Data."""

    def __init__(
        self,
        balance_info: dict[str, Any] | str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(balance_info, has_been_json_encoded)
        self.exchange_name = "BITFINEX"
        self.local_update_time = time.time()
        self.asset_type = asset_type
        self.balance_data = balance_info if has_been_json_encoded else None
        self.currency: str | None = None
        self.balance: float | None = None
        self.available: float | None = None
        self.reserved: float | None = None
        self.all_data: dict[str, Any] | None = None
        self.has_been_init_data = False

    def init_data(self) -> BitfinexSpotRequestBalanceData:
        if not self.has_been_json_encoded:
            if isinstance(self.balance_info, str):
                self.balance_data = json.loads(self.balance_info)
            else:
                self.balance_data = self.balance_info
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.balance_data, dict):
            self.currency = self.balance_data.get("currency")
            self.balance = self.balance_data.get("balance")
            self.available = self.balance_data.get("available")
            self.reserved = self.balance_data.get("reserved")

        self.has_been_init_data = True
        return self

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_asset_type(self) -> str:
        return self.asset_type

    def get_all_data(self) -> dict[str, Any]:
        if self.all_data is None:
            self.init_data()
            all_data: dict[str, Any] = {
                "exchange_name": self.exchange_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "currency": self.currency,
                "balance": self.balance,
                "available": self.available,
                "reserved": self.reserved,
            }
            self.all_data = all_data
        return self.all_data

    def __str__(self) -> str:
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()
