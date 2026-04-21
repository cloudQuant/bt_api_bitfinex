---
title: Home | bt_api_bitfinex
---

# bt_api_bitfinex Documentation

[![PyPI Version](https://img.shields.io/pypi/v/bt_api_bitfinex.svg)](https://pypi.org/project/bt_api_bitfinex/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bt_api_bitfinex.svg)](https://pypi.org/project/bt_api_bitfinex/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/cloudQuant/bt_api_bitfinex/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudQuant/bt_api_bitfinex/actions)
[![Docs](https://readthedocs.org/projects/bt-api-bitfinex/badge/?version=latest)](https://bt-api-bitfinex.readthedocs.io/)

## Overview

`bt_api_bitfinex` is the **Bitfinex exchange plugin** for the [bt_api](https://github.com/cloudQuant/bt_api_py) plugin ecosystem. It provides unified REST interfaces for Bitfinex **Spot** trading.

This package is a **runtime plugin dependency** for `bt_api` applications connecting to Bitfinex. It depends on [bt_api_base](https://github.com/cloudQuant/bt_api_base) for core infrastructure (registry, event bus, rate limiting).

## Key Benefits

- **Spot Trading**: Unified interface for Bitfinex spot markets
- **Dual API Modes**: Synchronous REST and asynchronous REST for high-throughput scenarios
- **Plugin Architecture**: Integrates via `ExchangeRegistry` — auto-registers at import time
- **Unified Data Model**: All responses normalized to bt_api_base container types (Ticker, OrderBook, Bar, Trade, Order, Balance...)
- **Config-Driven**: YAML-based exchange configuration — no hardcoded endpoints
- **HMAC-SHA2 Auth**: Full request signing for authenticated endpoints

## Architecture Overview

```
bt_api_bitfinex/
├── plugin.py                      # register_plugin() — bt_api plugin entry point
├── registry_registration.py        # register_bitfinex() — feeds / exchange_data registration
├── exchange_data/
│   └── bitfinex_exchange_data.py  # BitfinexExchangeDataSpot + REST endpoint definitions
├── feeds/
│   └── live_bitfinex/
│       ├── spot.py               # BitfinexRequestDataSpot — REST API implementation
│       └── request_base.py        # BitfinexRequestData base class
├── containers/                     # Normalized data container types
│   ├── orders/                   # OrderContainer
│   ├── balances/                 # AccountBalanceContainer
│   ├── bars/                    # BarContainer
│   ├── tickers/                 # TickContainer
│   ├── orderbooks/              # OrderBookContainer
│   ├── trades/                  # TradeContainer
│   └── accounts/               # AccountContainer
├── gateway/
│   └── adapter.py               # BitfinexGatewayAdapter
├── errors/
│   └── bitfinex_translator.py  # BitfinexErrorTranslator → bt_api_base.ApiError
└── configs/
    └── bitfinex.yaml           # REST paths, rate limits
```

## Installation

```bash
pip install bt_api_bitfinex
```

Or from source:

```bash
git clone https://github.com/cloudQuant/bt_api_bitfinex
cd bt_api_bitfinex
pip install -e .
```

## Quick Start

### Using bt_api Plugin Integration

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITFINEX___SPOT": {
        "api_key": "your_api_key",
        "secret": "your_secret",
    }
})

# Market data (public)
ticker = api.get_tick("BITFINEX___SPOT", "BTCUSD")

# Private endpoints (require API key)
balance = api.get_balance("BITFINEX___SPOT")
order = api.make_order(
    exchange_name="BITFINEX___SPOT",
    symbol="BTCUSD",
    volume=0.01,
    price=60000,
    order_type="limit"
)
```

### Using Direct Client

```python
from bt_api_bitfinex import BitfinexApi

client = BitfinexApi(
    api_key="your_api_key",
    secret_key="your_secret",
)

# Public market data
ticker = client.get_ticker("BTCUSD")

# Place order
order = client.make_order(
    symbol="BTCUSD",
    side="buy",
    order_type="limit",
    price=60000,
    qty=0.01,
)
```

## Supported Operations

### Market Data (Public)

| Operation | Description |
|-----------|-------------|
| `get_ticker` / `get_tick` | 24-hour rolling ticker |
| `get_depth` / `get_orderbook` | Order book depth |
| `get_kline` | K-line / candlestick data |
| `get_trade_history` | Recent trade history |
| `get_exchange_info` | Exchange trading rules and symbol info |
| `get_server_time` | Bitfinex server time |

### Account & Trading (Authenticated)

| Operation | Description |
|-----------|-------------|
| `get_account` / `get_balance` | Account info and balances |
| `get_open_orders` | All open orders |
| `query_order` | Query order by ID |
| `make_order` | Place a new order (LIMIT/MARKET) |
| `cancel_order` | Cancel an existing order |

## Rate Limits

| Endpoint Type | Limit |
|--------------|-------|
| Public endpoints | 60 requests/min |
| Authenticated endpoints | 90 requests/min |

## Error Handling

All Bitfinex API errors are translated to bt_api_base `ApiError` subclasses with descriptive messages. See [bt_api_base error handling](https://bt-api-base.readthedocs.io/).

## Resources

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-bitfinex.readthedocs.io/ |
| Chinese Docs | https://bt-api-bitfinex.readthedocs.io/zh/latest/ |
| GitHub Repository | https://github.com/cloudQuant/bt_api_bitfinex |
| PyPI Package | https://pypi.org/project/bt_api_bitfinex/ |
| Issue Tracker | https://github.com/cloudQuant/bt_api_bitfinex/issues |
| bt_api_base Docs | https://bt-api-base.readthedocs.io/ |
| Main Project | https://cloudquant.github.io/bt_api_py/ |

## License

MIT License — see [LICENSE](LICENSE).

## Support

- [GitHub Issues](https://github.com/cloudQuant/bt_api_bitfinex/issues) — bug reports and feature requests
- Email: yunjinqi@gmail.com
