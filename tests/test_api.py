import pytest
from unittest.mock import patch, Mock
from api import fetch_rates, API_URL

def test_fetch_rates_success():
    mock_response = Mock()
    mock_response.read.return_value = b'''
    {"Valute": {"USD": {"Value": 95.5, "Nominal": 1}, "EUR": {"Value": 105.0, "Nominal": 1}}}
    '''
    with patch('urllib.request.urlopen', return_value=mock_response):
        rates = fetch_rates()
        assert rates["USD"] == 95.5
        assert rates["EUR"] == 105.0

def test_fetch_rates_connection_error(temp_db, monkeypatch):
    def mock_save_rate(currency, rate):
        pass 
    monkeypatch.setattr('api.save_rate', mock_save_rate)
    monkeypatch.setattr('api.get_saved_rate', lambda x: None)

    with patch('urllib.request.urlopen', side_effect=ConnectionError):
        rates = fetch_rates()
        assert rates == {} 