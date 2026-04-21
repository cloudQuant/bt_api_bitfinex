# bt_api_bitfinex

[![PyPI Version](https://img.shields.io/pypi/v/bt_api_bitfinex.svg)](https://pypi.org/project/bt_api_bitfinex/)
[![Python Versions](https://img.shields.io/pypi/pyversions/bt_api_bitfinex.svg)](https://pypi.org/project/bt_api_bitfinex/)
[![License](https://img.shields.io/badge/License-MIT-blue.svg)](https://opensource.org/licenses/MIT)
[![CI](https://github.com/cloudQuant/bt_api_bitfinex/actions/workflows/ci.yml/badge.svg)](https://github.com/cloudQuant/bt_api_bitfinex/actions)
[![Docs](https://readthedocs.org/projects/bt-api-bitfinex/badge/?version=latest)](https://bt-api-bitfinex.readthedocs.io/)

---

> **Bitfinex exchange plugin for bt_api** — Unified REST API for Bitfinex **Spot** trading.

`bt_api_bitfinex` is a runtime plugin for [bt_api](https://github.com/cloudQuant/bt_api_py) that connects to **Bitfinex** exchange. It depends on [bt_api_base](https://github.com/cloudQuant/bt_api_base) for core infrastructure.

| Resource | Link |
|----------|------|
| English Docs | https://bt-api-bitfinex.readthedocs.io/ |
| Chinese Docs | https://bt-api-bitfinex.readthedocs.io/zh/latest/ |
| GitHub | https://github.com/cloudQuant/bt_api_bitfinex |
| PyPI | https://pypi.org/project/bt_api_bitfinex/ |
| Issues | https://github.com/cloudQuant/bt_api_bitfinex/issues |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| Main Project | https://github.com/cloudQuant/bt_api_py |

---

## Features

### Spot Trading

| Asset Type | Code | REST | Description |
|---|---|---|---|
| Spot | `BITFINEX___SPOT` | ✅ | Spot trading |

### REST API Modes

- **Synchronous REST** — Polling for order management, balance queries, historical data
- **Asynchronous REST** — High-throughput batch queries and concurrent requests

### Plugin Architecture

Auto-registers at import time via `ExchangeRegistry`. Works seamlessly with `BtApi`:

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITFINEX___SPOT": {
        "api_key": "your_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("BITFINEX___SPOT", "BTCUSD")
balance = api.get_balance("BITFINEX___SPOT")
order = api.make_order(exchange_name="BITFINEX___SPOT", symbol="BTCUSD", volume=0.01, price=60000, order_type="limit")
```

### Unified Data Containers

All exchange responses normalized to bt_api_base container types:

- `TickContainer` — 24hr rolling ticker
- `OrderBookContainer` — Order book depth
- `BarContainer` — K-line/candlestick
- `TradeContainer` — Individual trades
- `OrderContainer` — Order status and fills
- `AccountBalanceContainer` — Asset balances

---

## Installation

### From PyPI (Recommended)

```bash
pip install bt_api_bitfinex
```

### From Source

```bash
git clone https://github.com/cloudQuant/bt_api_bitfinex
cd bt_api_bitfinex
pip install -e .
```

### Requirements

- Python `3.9` – `3.14`
- `bt_api_base >= 0.15`
- `requests` for HTTP client
- `aiohttp` for async HTTP client

---

## Quick Start

### 1. Install

```bash
pip install bt_api_bitfinex
```

### 2. Get ticker (public — no API key needed)

```python
from bt_api_bitfinex import BitfinexApi

client = BitfinexApi()
ticker = client.get_ticker("BTCUSD")
print(f"BTCUSD price: {ticker.price}")
```

### 3. Place an order (requires API key)

```python
from bt_api_bitfinex import BitfinexApi

client = BitfinexApi(
    api_key="your_api_key",
    secret_key="your_secret",
)
client.connect()

order = client.make_order(
    symbol="BTCUSD",
    side="buy",
    order_type="limit",
    price=60000,
    qty=0.01,
)
print(f"Order placed: {order.order_id}")
```

### 4. bt_api Plugin Integration

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITFINEX___SPOT": {"api_key": "key", "secret": "secret"}
})

# REST calls
ticker = api.get_tick("BITFINEX___SPOT", "BTCUSD")
balance = api.get_balance("BITFINEX___SPOT")
```

---

## Architecture

```
bt_api_bitfinex/
├── plugin.py                      # register_plugin() — bt_api plugin entry point
├── registry_registration.py        # register_bitfinex() — feeds / exchange_data / balance_handler registration
├── exchange_data/
│   └── bitfinex_exchange_data.py # BitfinexExchangeDataSpot + endpoint definitions
├── feeds/
│   └── live_bitfinex/
│       ├── spot.py              # BitfinexRequestDataSpot — REST API implementation
│       └── request_base.py      # BitfinexRequestData base class
├── containers/                    # Normalized data container types
│   ├── orders/
│   ├── balances/
│   ├── bars/
│   ├── tickers/
│   ├── orderbooks/
│   ├── trades/
│   └── accounts/
├── gateway/
│   └── adapter.py              # BitfinexGatewayAdapter(PluginGatewayAdapter)
├── errors/
│   └── bitfinex_translator.py # BitfinexErrorTranslator → bt_api_base.ApiError
└── configs/
    └── bitfinex.yaml          # YAML config (REST paths, rate limits)
```

---

## Supported Operations

| Category | Operation | Notes |
|---|---|---|
| **Market Data** | `get_ticker` / `get_tick` | 24hr rolling ticker |
| | `get_depth` / `get_orderbook` | Order book depth |
| | `get_kline` | K-line/candlestick |
| | `get_trade_history` | Recent trade history |
| **Account** | `get_balance` | All asset balances |
| | `get_account` | Full account info |
| **Trading** | `make_order` | LIMIT/MARKET orders |
| | `cancel_order` | Cancel order |
| | `query_order` | Query order by ID |
| | `get_open_orders` | All open orders |

---

## Supported Bitfinex Symbols

All Bitfinex trading pairs are supported, including:

- `BTCUSD`, `ETHUSD`, `LTCUSD`, `XRPUSD` ...
- `BTCUSD`, `ETHUSD`, `LTCUSD` (with margin)

---

## Error Handling

All Bitfinex API errors are translated to bt_api_base `ApiError` subclasses with descriptive messages.

---

## Rate Limits

| Endpoint Type | Limit |
|---|---|
| Public endpoints | 60 requests/min |
| Authenticated endpoints | 90 requests/min |

---

## Documentation

| Doc | Link |
|-----|------|
| **English** | https://bt-api-bitfinex.readthedocs.io/ |
| **中文** | https://bt-api-bitfinex.readthedocs.io/zh/latest/ |
| API Reference | https://bt-api-bitfinex.readthedocs.io/api/ |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| Main Project | https://cloudquant.github.io/bt_api_py/ |

---

## License

MIT — see [LICENSE](LICENSE).

---

## Support

- [GitHub Issues](https://github.com/cloudQuant/bt_api_bitfinex/issues) — bug reports, feature requests
- Email: yunjinqi@gmail.com

---

---

## 中文

> **bt_api 的 Bitfinex 交易所插件** — 为 Bitfinex **现货**交易提供统一的 REST API。

`bt_api_bitfinex` 是 [bt_api](https://github.com/cloudQuant/bt_api_py) 的运行时插件，连接 **Bitfinex** 交易所。依赖 [bt_api_base](https://github.com/cloudQuant/bt_api_base) 提供核心基础设施。

| 资源 | 链接 |
|------|------|
| 英文文档 | https://bt-api-bitfinex.readthedocs.io/ |
| 中文文档 | https://bt-api-bitfinex.readthedocs.io/zh/latest/ |
| GitHub | https://github.com/cloudQuant/bt_api_bitfinex |
| PyPI | https://pypi.org/project/bt_api_bitfinex/ |
| 问题反馈 | https://github.com/cloudQuant/bt_api_bitfinex/issues |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| 主项目 | https://github.com/cloudQuant/bt_api_py |

---

## 功能特点

### 现货交易

| 资产类型 | 代码 | REST | 说明 |
|---|---|---|---|
| 现货 | `BITFINEX___SPOT` | ✅ | 现货交易 |

### REST API 模式

- **同步 REST** — 轮询：订单管理、余额查询、历史数据
- **异步 REST** — 高吞吐批量查询和并发请求

### 插件架构

通过 `ExchangeRegistry` 在导入时自动注册，与 `BtApi` 无缝协作：

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITFINEX___SPOT": {
        "api_key": "your_key",
        "secret": "your_secret",
    }
})

ticker = api.get_tick("BITFINEX___SPOT", "BTCUSD")
balance = api.get_balance("BITFINEX___SPOT")
order = api.make_order(exchange_name="BITFINEX___SPOT", symbol="BTCUSD", volume=0.01, price=60000, order_type="limit")
```

### 统一数据容器

所有交易所响应规范化为 bt_api_base 容器类型：

- `TickContainer` — 24小时滚动行情
- `OrderBookContainer` — 订单簿深度
- `BarContainer` — K线/蜡烛图
- `TradeContainer` — 逐笔成交
- `OrderContainer` — 订单状态和成交
- `AccountBalanceContainer` — 资产余额

---

## 安装

### 从 PyPI 安装（推荐）

```bash
pip install bt_api_bitfinex
```

### 从源码安装

```bash
git clone https://github.com/cloudQuant/bt_api_bitfinex
cd bt_api_bitfinex
pip install -e .
```

### 系统要求

- Python `3.9` – `3.14`
- `bt_api_base >= 0.15`
- `requests` HTTP 客户端
- `aiohttp` 异步 HTTP 客户端

---

## 快速开始

### 1. 安装

```bash
pip install bt_api_bitfinex
```

### 2. 获取行情（公开接口，无需 API key）

```python
from bt_api_bitfinex import BitfinexApi

client = BitfinexApi()
ticker = client.get_ticker("BTCUSD")
print(f"BTCUSD 价格: {ticker.price}")
```

### 3. 下单交易（需要 API key）

```python
from bt_api_bitfinex import BitfinexApi

client = BitfinexApi(
    api_key="your_api_key",
    secret_key="your_secret",
)
client.connect()

order = client.make_order(
    symbol="BTCUSD",
    side="buy",
    order_type="limit",
    price=60000,
    qty=0.01,
)
print(f"订单已下单: {order.order_id}")
```

### 4. bt_api 插件集成

```python
from bt_api_py import BtApi

api = BtApi(exchange_kwargs={
    "BITFINEX___SPOT": {"api_key": "key", "secret": "secret"}
})

# REST 调用
ticker = api.get_tick("BITFINEX___SPOT", "BTCUSD")
balance = api.get_balance("BITFINEX___SPOT")
```

---

## 架构

```
bt_api_bitfinex/
├── plugin.py                      # register_plugin() — bt_api 插件入口
├── registry_registration.py      # register_bitfinex() — feeds / exchange_data / balance_handler 注册
├── exchange_data/
│   └── bitfinex_exchange_data.py # BitfinexExchangeDataSpot + 端点定义
├── feeds/
│   └── live_bitfinex/
│       ├── spot.py             # BitfinexRequestDataSpot — REST API 实现
│       └── request_base.py     # BitfinexRequestData 基类
├── containers/                    # 规范化数据容器类型
│   ├── orders/
│   ├── balances/
│   ├── bars/
│   ├── tickers/
│   ├── orderbooks/
│   ├── trades/
│   └── accounts/
├── gateway/
│   └── adapter.py              # BitfinexGatewayAdapter(PluginGatewayAdapter)
├── errors/
│   └── bitfinex_translator.py # BitfinexErrorTranslator → bt_api_base.ApiError
└── configs/
    └── bitfinex.yaml          # YAML 配置（REST 路径、限流）
```

---

## 支持的操作

| 类别 | 操作 | 说明 |
|---|---|---|
| **行情数据** | `get_ticker` / `get_tick` | 24小时滚动行情 |
| | `get_depth` / `get_orderbook` | 订单簿深度 |
| | `get_kline` | K线/蜡烛图 |
| | `get_trade_history` | 近期成交历史 |
| **账户** | `get_balance` | 所有资产余额 |
| | `get_account` | 完整账户信息 |
| **交易** | `make_order` | 限价/市价订单 |
| | `cancel_order` | 撤销订单 |
| | `query_order` | 按ID查询订单 |
| | `get_open_orders` | 所有挂单 |

---

## 支持的 Bitfinex 交易对

全部 Bitfinex 交易对均支持，包括：

- `BTCUSD`, `ETHUSD`, `LTCUSD`, `XRPUSD` ...
- `BTCUSD`, `ETHUSD`, `LTCUSD` (保证金交易)

---

## 错误处理

所有 Bitfinex API 错误均翻译为 bt_api_base `ApiError` 子类，并提供描述性错误信息。

---

## 限流配置

| 端点类型 | 限制 |
|---|---|
| 公开端点 | 60 次/分钟 |
| 认证端点 | 90 次/分钟 |

---

## 文档

| 文档 | 链接 |
|-----|------|
| **英文文档** | https://bt-api-bitfinex.readthedocs.io/ |
| **中文文档** | https://bt-api-bitfinex.readthedocs.io/zh/latest/ |
| API 参考 | https://bt-api-bitfinex.readthedocs.io/api/ |
| bt_api_base | https://bt-api-base.readthedocs.io/ |
| 主项目 | https://cloudquant.github.io/bt_api_py/ |

---

## 许可证

MIT — 详见 [LICENSE](LICENSE)。

---

## 技术支持

- [GitHub Issues](https://github.com/cloudQuant/bt_api_bitfinex/issues) — bug 报告、功能请求
- 邮箱: yunjinqi@gmail.com
