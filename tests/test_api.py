import pytest
from unittest.mock import MagicMock
from api import fetch_rates


def test_fetch_rates_success(temp_db, monkeypatch):
    # Правильно мокаем urlopen с поддержкой timeout
    mock_context = MagicMock()
    mock_context.read.return_value = (
        b'{"Valute": {"USD": {"Value": 95.5, "Nominal": 1}, "EUR": {"Value": 105.0, "Nominal": 1}}}'
    )

    def mock_urlopen(url, timeout=None):
        return mock_context

    monkeypatch.setattr("urllib.request.urlopen", mock_urlopen)

    rates = fetch_rates()
    assert rates["USD"] == 95.5
    assert rates["EUR"] == 105.0


def test_fetch_rates_connection_error(temp_db, monkeypatch):
    def mock_urlopen(url, timeout=None):
        raise ConnectionError("Нет интернета")

    monkeypatch.setattr("urllib.request.urlopen", mock_urlopen)
    monkeypatch.setattr("api.get_saved_rate", lambda x: None)

    rates = fetch_rates()
    assert rates == {}
