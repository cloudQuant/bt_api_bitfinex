from unittest.mock import AsyncMock
import pytest
from bt_api_base.containers.requestdatas.request_data import RequestData
from bt_api_bitfinex.feeds.live_bitfinex.request_base import BitfinexRequestData


def test_bitfinex_request_allows_missing_extra_data(monkeypatch) -> None:
    request_data = BitfinexRequestData(
        public_key="public-key",
        private_key="secret-key",
        exchange_name="BITFINEX___SPOT",
    )

    monkeypatch.setattr(
        request_data,
        "http_request",
        lambda method, url, headers, body, timeout: [1710000000000],
    )

    result = request_data.request("GET /v2/platform/status")

    assert isinstance(result, RequestData)
    assert result.get_extra_data() == {}
    assert result.get_input_data() == [1710000000000]
