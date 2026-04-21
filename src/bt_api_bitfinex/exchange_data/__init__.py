"""Bitfinex Exchange Data Configuration."""

from __future__ import annotations

import json

from bt_api_base.containers.exchanges.exchange_data import ExchangeData
from bt_api_base.logging_factory import get_logger

logger = get_logger("bitfinex_exchange_data")


class BitfinexExchangeData(ExchangeData):
    """Base class for all Bitfinex exchange types."""

    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "BITFINEX"
        self.rest_url = ""
        self.acct_wss_url = ""
        self.wss_url = ""
        self.rest_paths = {}
        self.wss_paths = {}

        self.kline_periods = {
            "1m": "1m",
            "5m": "5m",
            "15m": "15m",
            "30m": "30m",
            "1h": "1h",
            "3h": "3h",
            "6h": "6h",
            "12h": "12h",
            "1d": "1D",
            "7d": "7D",
            "14d": "14D",
            "1M": "1M",
        }
        self.reverse_kline_periods = {v: k for k, v in self.kline_periods.items()}

        self.legal_currency = [
            "USD",
            "USDT",
            "BTC",
            "ETH",
            "EUR",
            "GBP",
            "JPY",
            "CAD",
            "AUD",
            "CHF",
        ]

    def get_symbol(self, symbol: str) -> str:
        if "-" in symbol:
            base, quote = symbol.split("-")
            return f"t{base}{quote}"
        return symbol

    def get_reverse_symbol(self, symbol: str) -> str:
        if symbol.startswith("t"):
            symbol = symbol[1:]
        if len(symbol) == 6:
            return f"{symbol[:3]}-{symbol[3:]}"
        return symbol

    def account_wss_symbol(self, symbol: str) -> str:
        return symbol.lower()

    def get_rest_path(self, key: str, **kwargs) -> str:
        if key not in self.rest_paths or self.rest_paths[key] == "":
            self.raise_path_error(self.exchange_name, key)
        path = self.rest_paths[key]
        if isinstance(path, list) and len(path) == 1:
            path = path[0]
        if isinstance(path, str):
            for param_key, param_value in kwargs.items():
                placeholder = f"<{param_key}>"
                if placeholder in path:
                    path = path.replace(placeholder, str(param_value))
        return path

    def get_wss_path(self, **kwargs) -> str:
        key = kwargs["topic"]
        if "symbol" in kwargs:
            kwargs["symbol"] = self.get_symbol(kwargs["symbol"])
        if "pair" in kwargs:
            kwargs["pair"] = self.get_symbol(kwargs["pair"])
        if "period" in kwargs:
            kwargs["period"] = self.get_period(kwargs["period"])

        if key not in self.wss_paths or self.wss_paths[key] == "":
            self.raise_path_error(self.exchange_name, key)
        req = self.wss_paths[key].copy()
        key = list(req.keys())[0]
        for k, v in kwargs.items():
            if isinstance(v, str):
                req[key] = [req[key][0].replace(f"<{k}>", v.lower())]
        new_value = []
        if "symbol_list" in kwargs:
            for symbol in kwargs["symbol_list"]:
                value = req[key]
                new_value.append(value[0].replace("<symbol>", self.get_symbol(symbol).lower()))
            req[key] = new_value
        return json.dumps(req)

    def get_period(self, period: str) -> str:
        return self.kline_periods.get(period, period)

    def get_reverse_period(self, period: str) -> str:
        return self.reverse_kline_periods.get(period, period)


class BitfinexExchangeDataSpot(BitfinexExchangeData):
    """Bitfinex Spot Trading Data Configuration."""

    def __init__(self) -> None:
        super().__init__()
        self.asset_type = "spot"
        self.exchange_name = "BITFINEX___SPOT"
        self.rest_url = "https://api-pub.bitfinex.com/v2"
        self.wss_url = "wss://api.bitfinex.com/ws/v2"
        self.acct_wss_url = "wss://api.bitfinex.com/ws/v2"

        self.rest_paths = {
            "base_url": "https://api-pub.bitfinex.com/v2",
            "ticker": "GET /ticker/{symbol}",
            "orderbook": "GET /book/{symbol}/{precision}",
            "klines": "GET /candles/trade:{timeframe}:{symbol}/hist",
            "trade_history": "GET /trades/{symbol}/hist",
            "account_balance": "POST /auth/r/wallets",
            "open_orders": "POST /auth/r/orders",
            "make_order": "POST /auth/w/order/submit",
            "cancel_order": "POST /auth/w/order/cancel",
            "order_status": "POST /auth/r/orders/{symbol}",
            "query_order": "GET /auth/r/orders/{id}",
            "get_order": "GET /auth/r/orders/{id}",
            "get_exchange_info": "GET /pub/symbols",
            "trade_history_auth": "POST /auth/r/trades/{symbol}/hist",
            "platform_status": "GET /platform/status",
            "symbols": "GET /conf/pub:list:pair:exchange",
            "currencies": "GET /conf/pub:list:currency",
        }

        self.wss_paths = {
            "ticker": {"params": ["ticker:{symbol}"], "method": "SUBSCRIBE", "id": 1},
            "trades": {"params": ["trades:{symbol}"], "method": "SUBSCRIBE", "id": 1},
            "orderbook": {
                "params": ["book:{symbol}:{precision}:{len}"],
                "method": "SUBSCRIBE",
                "id": 1,
            },
            "klines": {
                "params": ["candle_raw_{symbol}:trade:{period}"],
                "method": "SUBSCRIBE",
                "id": 1,
            },
            "auth": {"params": [], "method": "SUBSCRIBE", "id": 1},
        }

        self.symbol_mappings = {
            "BTC-USD": "tBTCUSD",
            "ETH-USD": "tETHUSD",
            "ETH-BTC": "tETHBTC",
            "XRP-USD": "tXRPUSD",
            "LTC-USD": "tLTCUSD",
            "ADA-USD": "tADAUSD",
            "DOT-USD": "tDOTUSD",
            "SOL-USD": "tSOLUSD",
            "MATIC-USD": "tMATICUSD",
            "AVAX-USD": "tAVAXUSD",
            "LINK-USD": "tLINKUSD",
            "UNI-USD": "tUNIUSD",
            "BCH-USD": "tBCHUSD",
            "EOS-USD": "tEOSUSD",
            "ETC-USD": "tETCUSD",
            "XLM-USD": "tXLMUSD",
            "THETA-USD": "tTHETAUSD",
            "VET-USD": "tVETUSD",
            "FIL-USD": "tFILUSD",
            "TRX-USD": "tTRXUSD",
            "XTZ-USD": "tXTZUSD",
            "ATOM-USD": "tATOMUSD",
            "NEO-USD": "tNEOUSD",
            "AAVE-USD": "tAAVEUSD",
            "COMP-USD": "tCOMPUSD",
            "MKR-USD": "tMKRUSD",
            "SNX-USD": "tSNXUSD",
            "YFI-USD": "tYFIUSD",
            "CRV-USD": "tCRVUSD",
            "SUSHI-USD": "tSUSHIUSD",
            "1INCH-USD": "t1INCHUSD",
            "ENJ-USD": "tENJUSD",
            "BAT-USD": "tBATUSD",
            "ZEC-USD": "tZECUSD",
            "DASH-USD": "tDASHUSD",
            "ZRX-USD": "tZRXUSD",
            "KNC-USD": "tKNCUSD",
            "OMG-USD": "tOMGUSD",
            "REN-USD": "tRENUSD",
            "MLN-USD": "tMLNUSD",
            "MANA-USD": "tMANAUSD",
            "SAND-USD": "tSANDUSD",
            "AXS-USD": "tAXSUSD",
            "GRT-USD": "tGRTUSD",
            "CHZ-USD": "tCHZUSD",
            "RUNE-USD": "tRUNEUSD",
            "NKN-USD": "tNKNUSD",
            "BNT-USD": "tBNTUSD",
            "KAVA-USD": "tKAVAUSD",
            "BAND-USD": "tBANDUSD",
            "ALPHA-USD": "tALPHAUSD",
            "CTSI-USD": "tCTSIUSD",
            "RVN-USD": "tRVNUSD",
            "CTK-USD": "tCTKUSD",
            "NU-USD": "tNUUSD",
            "CRO-USD": "tCROUSD",
            "LEO-USD": "tLEOUSD",
            "LRC-USD": "tLRCUSD",
            "SKL-USD": "tSKLUSD",
            "UMA-USD": "tUMAUSD",
            "PERP-USD": "tPERPUSD",
            "BADGER-USD": "tBADGERUSD",
            "FEI-USD": "tFEIUSD",
            "ANKR-USD": "tANKRUSD",
            "HNT-USD": "tHNTUSD",
            "FTT-USD": "tFTTUSD",
            "FTM-USD": "tFTMUSD",
            "CELO-USD": "tCELOUSD",
            "HEX-USD": "tHEXUSD",
            "EGLD-USD": "tEGLDUSD",
            "HBAR-USD": "tHBARUSD",
            "AMP-USD": "tAMPUSD",
            "TFUEL-USD": "tTFUELUSD",
            "HT-USD": "tHTUSD",
            "IOTA-USD": "tIOTAUSD",
            "VTHO-USD": "tVTHOUSD",
            "XVG-USD": "tXVGUSD",
            "WAVES-USD": "tWAVESUSD",
            "ZIL-USD": "tZILUSD",
            "DFI-USD": "tDFIUSD",
            "LUNA-USD": "tLUNAUSD",
            "BUSD-USD": "tBUSDUSD",
            "USDC-USD": "tUSDCUSD",
            "PAX-USD": "tPAXUSD",
            "GUSD-USD": "tGUSDUSD",
            "HUSD-USD": "tHUSDUSD",
            "PAXG-USD": "tPAXGUSD",
            "tXAUUSD": "tXAUUSD",
            "tXAGUSD": "tXAGUSD",
            "fUSD": "fUSD",
            "fUSDT": "fUSDT",
            "fBTC": "fBTC",
            "fETH": "fETH",
        }

        self.reverse_symbol_mappings = {v: k for k, v in self.symbol_mappings.items()}

    def get_symbol(self, symbol: str) -> str:
        if symbol in self.symbol_mappings:
            return self.symbol_mappings[symbol]
        if "-" in symbol:
            base, quote = symbol.split("-")
            return f"t{base}{quote}"
        return symbol

    def get_reverse_symbol(self, symbol: str) -> str:
        if symbol in self.reverse_symbol_mappings:
            return self.reverse_symbol_mappings[symbol]
        if symbol.startswith("t"):
            symbol = symbol[1:]
        if len(symbol) >= 6:
            for i in range(3, len(symbol) - 2):
                base = symbol[:i]
                quote = symbol[i:]
                if base in self.legal_currency or quote in self.legal_currency:
                    return f"{base}-{quote}"
        return symbol

    def get_precision(self, symbol: str) -> str:
        return "P0"

    def get_orderbook_length(self, symbol: str) -> str:
        return "25"


class BitfinexExchangeDataMargin(BitfinexExchangeData):
    """Bitfinex Margin Trading Data Configuration."""

    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "BITFINEX___MARGIN"
        self.rest_url = "https://api-pub.bitfinex.com/v2"
        self.wss_url = "wss://api.bitfinex.com/ws/v2"
        self.acct_wss_url = "wss://api.bitfinex.com/ws/v2"


class BitfinexExchangeDataFutures(BitfinexExchangeData):
    """Bitfinex Futures Trading Data Configuration."""

    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "BITFINEX___FUTURES"
        self.rest_url = "https://api-pub.bitfinex.com/v2"
        self.wss_url = "wss://api.bitfinex.com/ws/v2"
        self.acct_wss_url = "wss://api.bitfinex.com/ws/v2"


class BitfinexExchangeDataFunding(BitfinexExchangeData):
    """Bitfinex Funding Data Configuration."""

    def __init__(self) -> None:
        super().__init__()
        self.exchange_name = "BITFINEX___FUNDING"
        self.rest_url = "https://api-pub.bitfinex.com/v2"
        self.wss_url = "wss://api.bitfinex.com/ws/v2"
        self.acct_wss_url = "wss://api.bitfinex.com/ws/v2"
