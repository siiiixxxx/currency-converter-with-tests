import pytest
from unittest.mock import MagicMock, patch
from api import fetch_rates


def test_fetch_rates_success(temp_db, monkeypatch):
    # Мокаем весь процесс: и urlopen, и json.loads
    fake_data = {
        "Valute": {
            "USD": {"Value": 95.5, "Nominal": 1},
            "EUR": {"Value": 105.0, "Nominal": 1},
            "CNY": {"Value": 13.3, "Nominal": 1},
            "GBP": {"Value": 120.0, "Nominal": 1},
        }
    }

    mock_response = MagicMock()
    mock_response.read.return_value = b"whatever"  # не важно что

    with patch("urllib.request.urlopen", return_value=mock_response), patch(
        "json.loads", return_value=fake_data
    ):

        rates = fetch_rates()

    assert rates == {"USD": 95.5, "EUR": 105.0, "CNY": 13.3, "GBP": 120.0}


def test_fetch_rates_connection_error(temp_db, monkeypatch):
    with patch("urllib.request.urlopen", side_effect=ConnectionError), patch(
        "api.get_saved_rate", return_value=None
    ):

        rates = fetch_rates()

    assert rates == {}
