"""Bitfinex Account Data Container."""

from __future__ import annotations

import json
import time
from typing import Any

from bt_api_base.containers.accounts.account import AccountData


class BitfinexSpotRequestAccountData(AccountData):
    """Bitfinex Spot Request Account Data."""

    def __init__(
        self,
        account_info: dict[str, Any] | str,
        asset_type: str,
        has_been_json_encoded: bool = False,
    ) -> None:
        super().__init__(account_info, has_been_json_encoded)
        self.exchange_name = "BITFINEX"
        self.local_update_time = time.time()
        self.asset_type = asset_type
        self.account_data = account_info if has_been_json_encoded else None
        self.all_data: dict[str, Any] | None = None
        self.has_been_init_data = False

    def init_data(self):
        if not self.has_been_json_encoded:
            if isinstance(self.account_info, str):
                self.account_data = json.loads(self.account_info)
            else:
                self.account_data = self.account_info
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self
        data = self.account_data or {}
        self.account_id = data.get("id")
        self.account_type = data.get("type")
        self.currency = data.get("currency")
        self.balance = data.get("balance")
        self.available = data.get("available")
        self.timestamp = data.get("timestamp")
        self.has_been_init_data = True
        return self

    def get_all_data(self) -> dict[str, Any]:
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "account_data": self.account_data,
                "account_id": getattr(self, "account_id", None),
                "account_type": getattr(self, "account_type", None),
                "currency": getattr(self, "currency", None),
                "balance": getattr(self, "balance", None),
                "available": getattr(self, "available", None),
                "timestamp": getattr(self, "timestamp", None),
            }
        return self.all_data

    def __str__(self) -> str:
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self) -> str:
        return self.__str__()

    def get_exchange_name(self) -> str:
        return self.exchange_name

    def get_asset_type(self) -> str:
        return self.asset_type


BitfinexSpotWssAccountData = BitfinexSpotRequestAccountData
