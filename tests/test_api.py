import pytest
from unittest.mock import patch, MagicMock
from api import fetch_rates


def test_fetch_rates_success(temp_db, monkeypatch):
    mock_response = MagicMock()
    mock_response.__enter__.return_value.read.return_value = (
        b'{"Valute": {"USD": {"Value": 95.5, "Nominal": 1}, "EUR": {"Value": 105.0, "Nominal": 1}}}'
    )
    mock_response.__enter__.return_value.__exit__.return_value = None

    monkeypatch.setattr("urllib.request.urlopen", lambda x: mock_response)

    rates = fetch_rates()
    assert rates["USD"] == 95.5
    assert rates["EUR"] == 105.0


def test_fetch_rates_connection_error(temp_db, monkeypatch):
    monkeypatch.setattr("urllib.request.urlopen", lambda x: (_ for _ in ()).throw(ConnectionError))
    monkeypatch.setattr("api.get_saved_rate", lambda x: None)

    rates = fetch_rates()
    assert rates == {}
