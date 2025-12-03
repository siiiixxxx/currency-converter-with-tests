import pytest
from main import CurrencyConverterApp
import tkinter as tk

@pytest.fixture
def app(monkeypatch):
    monkeypatch.setattr('tkinter.messagebox.showerror', lambda *args: None)
    app = CurrencyConverterApp()
    app.update()
    return app

def test_calculate_loan_success(app, monkeypatch):
    monkeypatch.setattr('api.fetch_rates', lambda: {"USD": 95.0})
    app.loan_var.set("100000")
    app.time_var.set("12")
    app.interest_var.set("10")
    
    app.calculate_loan()
    
    monthly_text = app.monthly_label.cget("text")
    assert "8" in monthly_text or "9" in monthly_text  

def test_convert_success(app, monkeypatch):
    monkeypatch.setattr('api.fetch_rates', lambda: {"USD": 95.0})
    app.rates = {"USD": 95.0}
    app.monthly_label.config(text="95000 ₽")
    app.target_var.set("USD")
    
    app.convert()
    
    result = app.result_label.cget("text")
    assert "1000" in result or "999" in result or "1001" in result