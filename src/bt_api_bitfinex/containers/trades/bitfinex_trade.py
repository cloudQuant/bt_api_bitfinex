"""Bitfinex Trade Data Container."""

from __future__ import annotations

import json
import time

from bt_api_base.containers.trades.trade import TradeData


class BitfinexRequestTradeData(TradeData):
    """Bitfinex Request Trade Data."""

    def __init__(self, trade_info, symbol_name, asset_type, has_been_json_encoded=False):
        super().__init__(trade_info, has_been_json_encoded)
        self.exchange_name = "BITFINEX"
        self.local_update_time = time.time()
        self.symbol_name = symbol_name
        self.asset_type = asset_type
        self.trade_data = trade_info if has_been_json_encoded else None
        self.trade_id = None
        self.price = None
        self.amount = None
        self.timestamp = None
        self.side = None
        self.fee = None
        self.has_been_init_data = False

    def init_data(self):
        if not self.has_been_json_encoded:
            self.trade_data = json.loads(self.trade_info)
            self.has_been_json_encoded = True
        if self.has_been_init_data:
            return self

        if isinstance(self.trade_data, list) and len(self.trade_data) >= 4:
            self.trade_id = str(self.trade_data[0])
            self.timestamp = self.trade_data[1] / 1000 if self.trade_data[1] else None
            self.amount = abs(float(self.trade_data[2])) if self.trade_data[2] else None
            self.price = float(self.trade_data[3]) if self.trade_data[3] else None
            self.side = "BUY" if self.trade_data[2] > 0 else "SELL"
            if len(self.trade_data) > 5:
                self.fee = self.trade_data[5]

        self.has_been_init_data = True
        return self

    def get_all_data(self):
        if self.all_data is None:
            self.init_data()
            self.all_data = {
                "exchange_name": self.exchange_name,
                "symbol_name": self.symbol_name,
                "asset_type": self.asset_type,
                "local_update_time": self.local_update_time,
                "trade_id": self.trade_id,
                "price": self.price,
                "amount": self.amount,
                "timestamp": self.timestamp,
                "side": self.side,
                "fee": self.fee,
            }
        return self.all_data

    def __str__(self):
        self.init_data()
        return json.dumps(self.get_all_data())

    def __repr__(self):
        return self.__str__()

    def get_exchange_name(self):
        return self.exchange_name

    def get_symbol_name(self):
        return self.symbol_name

    def get_asset_type(self):
        return self.asset_type

    def get_trade_id(self):
        return self.trade_id

    def get_price(self):
        return self.price

    def get_amount(self):
        return self.amount

    def get_timestamp(self):
        return self.timestamp

    def get_side(self):
        return self.side

    def get_fee(self):
        return self.fee
