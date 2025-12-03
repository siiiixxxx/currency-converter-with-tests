import json
import urllib.request
from db import save_rate, get_saved_rate

API_URL = "https://www.cbr-xml-daily.ru/daily_json.js"


def fetch_rates() -> dict:

    try:
        with urllib.request.urlopen(API_URL, timeout=10) as response:
            data = json.loads(response.read().decode())

        rates = {}
        for code in ['USD', 'EUR', 'CNY', 'GBP']:
            if code in data['Valute']:
                info = data['Valute'][code]
                rate = info['Value']
                if info['Nominal'] != 1:
                    rate = rate / info['Nominal']
                rates[code] = round(rate, 4)
                save_rate(code, rate)

        return rates

    except Exception as e:
        print(f"API error: {e}. Using DB cache.")
        return {
            code: get_saved_rate(code) or 0.0
            for code in ['USD', 'EUR', 'CNY', 'GBP']
            if get_saved_rate(code)
        }