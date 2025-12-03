import pytest
from db import save_rate, get_saved_rate
from datetime import datetime


def test_init_db_creates_table(temp_db):
    from db import init_db

    init_db()
    assert get_saved_rate("USD") is None


def test_save_rate_new_record(temp_db):
    save_rate("USD", 95.5)
    assert get_saved_rate("USD") == 95.5


def test_save_rate_update_existing(temp_db):
    save_rate("EUR", 100.0)
    save_rate("EUR", 105.5)
    assert get_saved_rate("EUR") == 105.5


def test_save_rate_multiple_currencies(temp_db):
    save_rate("USD", 95.0)
    save_rate("EUR", 105.0)
    save_rate("CNY", 13.5)
    assert get_saved_rate("USD") == 95.0
    assert get_saved_rate("EUR") == 105.0
    assert get_saved_rate("CNY") == 13.5


def test_get_saved_rate_nonexistent_currency(temp_db):
    assert get_saved_rate("XXX") is None


def test_save_rate_sql_injection_protection(temp_db):
    save_rate("USD'; DROP TABLE rates;--", 999.0)
    assert get_saved_rate("USD'; DROP TABLE rates;--") == 999.0
