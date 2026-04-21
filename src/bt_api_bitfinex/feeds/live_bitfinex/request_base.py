"""Bitfinex REST API request base class."""

from __future__ import annotations

import hashlib
import hmac
import json
import time
from typing import Any
from urllib.parse import urlencode

from bt_api_base.containers.balances.balance import BalanceData
from bt_api_base.containers.bars.bar import BarData
from bt_api_base.containers.exchanges.exchange_data import ExchangeData
from bt_api_base.containers.orderbooks.orderbook import OrderBookData
from bt_api_base.containers.orders.order import OrderData
from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_base.containers.trades.trade import TradeData
from bt_api_base.exceptions import QueueNotInitializedError
from bt_api_base.feeds.capability import Capability
from bt_api_base.feeds.feed import Feed
from bt_api_base.feeds.http_client import HttpClient
from bt_api_base.functions.utils import update_extra_data
from bt_api_base.logging_factory import get_logger

from bt_api_bitfinex.containers.balances.bitfinex_balance import BitfinexSpotRequestBalanceData
from bt_api_bitfinex.containers.bars.bitfinex_bar import BitfinexRequestBarData
from bt_api_bitfinex.containers.orderbooks.bitfinex_orderbook import BitfinexRequestOrderBookData
from bt_api_bitfinex.containers.orders.bitfinex_order import BitfinexRequestOrderData
from bt_api_bitfinex.containers.trades.bitfinex_trade import BitfinexRequestTradeData
from bt_api_bitfinex.exchange_data import BitfinexExchangeDataSpot
from bt_api_bitfinex.tickers import BitfinexRequestTickerData


class BitfinexRequestData(Feed):
    """Bitfinex REST API base class.

    Uses Feed.http_request() for HTTP calls, supports "METHOD /path" format.
    Authentication uses HMAC SHA384 with bfx-apikey / bfx-signature headers.
    """

    @classmethod
    def _capabilities(cls) -> set:
        return {
            Capability.GET_TICK,
            Capability.GET_DEPTH,
            Capability.GET_KLINE,
            Capability.MAKE_ORDER,
            Capability.CANCEL_ORDER,
            Capability.QUERY_ORDER,
            Capability.QUERY_OPEN_ORDERS,
            Capability.GET_DEALS,
            Capability.GET_BALANCE,
            Capability.GET_ACCOUNT,
            Capability.GET_EXCHANGE_INFO,
            Capability.GET_SERVER_TIME,
        }

    def __init__(self, data_queue: Any = None, **kwargs: Any) -> None:
        super().__init__(data_queue, **kwargs)
        self.data_queue = data_queue
        self.api_key = kwargs.get("api_key") or kwargs.get("public_key")
        self.api_secret = kwargs.get("api_secret") or kwargs.get("private_key")
        self.asset_type = kwargs.get("asset_type", "SPOT")
        self.exchange_name = kwargs.get("exchange_name", "BITFINEX___SPOT")
        self.logger_name = kwargs.get("logger_name", "bitfinex_spot_feed.log")
        self._params = kwargs.get("exchange_data", BitfinexExchangeDataSpot())

        self.request_logger = get_logger("bitfinex_spot_feed")
        self.async_logger = get_logger("bitfinex_spot_feed")
        self._http_client = HttpClient(venue=self.exchange_name, timeout=30)

    def sign(self, path, nonce, body=""):
        signature_payload = f"/api{path}{nonce}{body}"
        signature = hmac.new(
            self.api_secret.encode(), signature_payload.encode(), hashlib.sha384
        ).hexdigest()
        return signature

    def push_data_to_queue(self, data):
        if self.data_queue is not None:
            self.data_queue.put(data)
        else:
            raise QueueNotInitializedError("data_queue not initialized")

    def request(self, path, params=None, body=None, extra_data=None, timeout=10, is_sign=False):
        if params is None:
            params = {}
        if extra_data is None:
            extra_data = {}
        method, endpoint = path.split(" ", 1)

        query_string = urlencode(params) if params else ""
        url = f"{self._params.rest_url}{endpoint}"
        if query_string:
            url = f"{url}?{query_string}"

        headers = {"Content-Type": "application/json"}
        if is_sign and self.api_key and self.api_secret:
            nonce = str(int(time.time() * 1000000))
            body_str = json.dumps(body) if body else ""
            sig = self.sign(endpoint, nonce, body_str)
            headers.update(
                {
                    "bfx-apikey": self.api_key,
                    "bfx-nonce": nonce,
                    "bfx-signature": sig,
                }
            )

        response = self.http_request(method, url, headers, body, timeout)
        return RequestData(response, extra_data)

    async def async_request(
        self, path, params=None, body=None, extra_data=None, timeout=10, is_sign=False
    ):
        if params is None:
            params = {}
        if extra_data is None:
            extra_data = {}
        method, endpoint = path.split(" ", 1)

        query_string = urlencode(params) if params else ""
        url = f"{self._params.rest_url}{endpoint}"
        if query_string:
            url = f"{url}?{query_string}"

        headers = {"Content-Type": "application/json"}
        if is_sign and self.api_key and self.api_secret:
            nonce = str(int(time.time() * 1000000))
            body_str = json.dumps(body) if body else ""
            sig = self.sign(endpoint, nonce, body_str)
            headers.update(
                {
                    "bfx-apikey": self.api_key,
                    "bfx-nonce": nonce,
                    "bfx-signature": sig,
                }
            )

        response = await self._http_client.async_request(
            method=method,
            url=url,
            headers=headers,
            json_data=body if method in ["POST", "PUT", "DELETE"] else None,
        )

        self.async_logger.info(f"Async Request: {method} {url}")
        return RequestData(response, extra_data)

    def async_callback(self, future):
        try:
            result = future.result()
            self.push_data_to_queue(result)
        except Exception as e:
            self.async_logger.warning(f"async_callback::{e}")

    def _get_server_time(self, extra_data=None, **kwargs):
        request_type = "get_server_time"
        path = self._params.get_rest_path(request_type)
        params = {}

        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": request_type,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_server_time_normalize_function,
            },
        )
        return path, params, extra_data

    @staticmethod
    def _get_server_time_normalize_function(input_data, extra_data):
        status = input_data is not None
        server_time = None
        if status and isinstance(input_data, list) and len(input_data) > 0:
            server_time = input_data[0]
        return [{"server_time": server_time}], status

    def _get_exchange_info(self, symbol=None, extra_data=None, **kwargs):
        request_type = "get_exchange_info"
        path = self._params.get_rest_path(request_type)
        params = {}

        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": request_type,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_exchange_info_normalize_function,
            },
        )
        return path, params, extra_data

    @staticmethod
    def _get_exchange_info_normalize_function(input_data, extra_data):
        status = input_data is not None
        symbols = input_data if isinstance(input_data, list) else []
        return [{"symbols": symbols}], status

    def _get_ticker(self, symbol, extra_data=None, **kwargs):
        request_symbol = self._params.get_symbol(symbol)
        request_type = "get_tick"
        path = self._params.get_rest_path(request_type)
        path = path.replace("{symbol}", request_symbol)
        params = {}

        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": request_type,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_ticker_normalize_function,
            },
        )
        return path, params, extra_data

    @staticmethod
    def _get_ticker_normalize_function(input_data, extra_data):
        status = input_data is not None
        symbol_name = extra_data["symbol_name"]
        asset_type = extra_data["asset_type"]
        if isinstance(input_data, list) and len(input_data) >= 8:
            data = [BitfinexRequestTickerData(input_data, symbol_name, asset_type, True)]
        else:
            data = []
        return data, status

    def _get_order_book(self, symbol, precision="P0", length="25", extra_data=None, **kwargs):
        request_symbol = self._params.get_symbol(symbol)
        request_type = "get_depth"
        path = self._params.get_rest_path(request_type)
        path = path.replace("{symbol}", request_symbol)
        path = path.replace("{precision}", precision)
        path = path.replace("{len}", length)
        params = {}

        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": request_type,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_order_book_normalize_function,
            },
        )
        return path, params, extra_data

    @staticmethod
    def _get_order_book_normalize_function(input_data, extra_data):
        status = input_data is not None
        symbol_name = extra_data["symbol_name"]
        asset_type = extra_data["asset_type"]
        if isinstance(input_data, list):
            data = [BitfinexRequestOrderBookData(input_data, symbol_name, asset_type, True)]
        else:
            data = []
        return data, status

    def _get_klines(self, symbol, period="1m", limit=100, extra_data=None, **kwargs):
        request_symbol = self._params.get_symbol(symbol)
        request_period = self._params.get_period(period)
        request_type = "get_kline"
        path = self._params.get_rest_path(request_type)
        path = path.replace("{symbol}", request_symbol)
        path = path.replace("{period}", request_period)
        path = path.replace("{limit}", str(limit))
        path = path.replace("&start={start}", "").replace("&end={end}", "")
        params = {}

        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": request_type,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_klines_normalize_function,
            },
        )
        return path, params, extra_data

    @staticmethod
    def _get_klines_normalize_function(input_data, extra_data):
        status = input_data is not None
        symbol_name = extra_data["symbol_name"]
        asset_type = extra_data["asset_type"]
        if isinstance(input_data, list):
            data = [BitfinexRequestBarData(input_data, symbol_name, asset_type, True)]
        else:
            data = []
        return data, status

    def _get_trade_history(self, symbol, limit=100, extra_data=None, **kwargs):
        request_symbol = self._params.get_symbol(symbol)
        request_type = "get_historical_trades"
        path = self._params.get_rest_path(request_type)
        path = path.replace("{symbol}", request_symbol)
        path = path.replace("{limit}", str(limit))
        params = {}

        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": request_type,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_trade_history_normalize_function,
            },
        )
        return path, params, extra_data

    @staticmethod
    def _get_trade_history_normalize_function(input_data, extra_data):
        status = input_data is not None
        symbol_name = extra_data["symbol_name"]
        asset_type = extra_data["asset_type"]
        if isinstance(input_data, list):
            data = [BitfinexRequestTradeData(input_data, symbol_name, asset_type, True)]
        else:
            data = []
        return data, status

    def _make_order(
        self,
        symbol,
        vol,
        price=None,
        order_type="buy-limit",
        offset="open",
        post_only=False,
        client_order_id=None,
        extra_data=None,
        **kwargs,
    ):
        request_symbol = self._params.get_symbol(symbol)
        request_type = "make_order"
        path = self._params.get_rest_path(request_type)

        side, order_type_subtype = order_type.split("-")

        params = {
            "type": order_type_subtype.upper(),
            "symbol": request_symbol,
            "amount": str(vol),
            "flags": 64 if post_only else 0,
        }

        if price is not None and order_type_subtype != "market":
            params["price"] = str(price)

        if client_order_id is not None:
            params["cid"] = int(client_order_id)

        if "lev" in kwargs:
            params["lev"] = kwargs["lev"]

        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": request_type,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "post_only": post_only,
                "normalize_function": self._make_order_normalize_function,
            },
        )
        return path, params, extra_data

    @staticmethod
    def _make_order_normalize_function(input_data, extra_data):
        status = input_data is not None
        symbol_name = extra_data["symbol_name"]
        asset_type = extra_data["asset_type"]
        if isinstance(input_data, list):
            data = [BitfinexRequestOrderData(i, symbol_name, asset_type, True) for i in input_data]
        elif isinstance(input_data, dict):
            data = [BitfinexRequestOrderData(input_data, symbol_name, asset_type, True)]
        else:
            data = []
        return data, status

    def _cancel_order(
        self, symbol=None, order_id=None, client_order_id=None, extra_data=None, **kwargs
    ):
        request_type = "cancel_order"
        path = self._params.get_rest_path(request_type)
        params = {}
        if order_id is not None:
            params["id"] = order_id
        if client_order_id is not None:
            params["cid"] = client_order_id

        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": request_type,
                "order_id": order_id,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._cancel_order_normalize_function,
            },
        )
        return path, params, extra_data

    @staticmethod
    def _cancel_order_normalize_function(input_data, extra_data):
        status = input_data is not None
        asset_type = extra_data["asset_type"]
        if isinstance(input_data, list) and len(input_data) > 0:
            order_id = extra_data.get("order_id")
            cancel_data = {"id": input_data[0], "status": "SUCCESS"}
            data = [BitfinexRequestOrderData(cancel_data, f"order_{order_id}", asset_type, True)]
        else:
            data = []
        return data, status

    def _get_order(
        self, symbol=None, order_id=None, client_order_id=None, extra_data=None, **kwargs
    ):
        request_type = "get_order"
        path = self._params.get_rest_path(request_type)
        if order_id is not None:
            path = path.replace("{id}", str(order_id))
        params = {}

        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": request_type,
                "order_id": order_id,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_order_normalize_function,
            },
        )
        return path, params, extra_data

    @staticmethod
    def _get_order_normalize_function(input_data, extra_data):
        status = input_data is not None
        symbol_name = extra_data.get("symbol_name")
        asset_type = extra_data["asset_type"]
        if isinstance(input_data, (list, dict)):
            data = [BitfinexRequestOrderData(input_data, symbol_name, asset_type, True)]
        else:
            data = []
        return data, status

    def _get_open_orders(self, symbol=None, extra_data=None, **kwargs):
        request_type = "get_open_orders"
        path = self._params.get_rest_path(request_type)
        params = {}
        if symbol:
            request_symbol = self._params.get_symbol(symbol)
            path = path.replace("{symbol}", request_symbol)

        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": request_type,
                "symbol_name": symbol,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_open_orders_normalize_function,
            },
        )
        return path, params, extra_data

    @staticmethod
    def _get_open_orders_normalize_function(input_data, extra_data):
        status = input_data is not None
        symbol_name = extra_data.get("symbol_name")
        asset_type = extra_data["asset_type"]
        if isinstance(input_data, list):
            data = [BitfinexRequestOrderData(input_data, symbol_name, asset_type, True)]
        else:
            data = []
        return data, status

    def _get_account(self, extra_data=None, **kwargs):
        request_type = "get_account"
        path = self._params.get_rest_path(request_type)
        params = {}

        extra_data = update_extra_data(
            extra_data,
            **{
                "request_type": request_type,
                "asset_type": self.asset_type,
                "exchange_name": self.exchange_name,
                "normalize_function": self._get_account_normalize_function,
            },
        )
        return path, params, extra_data

    @staticmethod
    def _get_account_normalize_function(input_data, extra_data):
        status = input_data is not None
        asset_type = extra_data["asset_type"]
        if isinstance(input_data, list):
            data = [BitfinexSpotRequestBalanceData(input_data, asset_type, True)]
        else:
            data = []
        return data, status
