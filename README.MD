# Калькулятор кредита с конвертацией валют

Простое десктопное приложение на Tkinter, которое:
- Считает ежемесячный платёж по кредиту (аннуитетный расчёт)
- Конвертирует платёж в USD, EUR, CNY, GBP по курсу ЦБ РФ
- Кеширует курсы в SQLite
- Работает даже без интернета (берёт последние сохранённые курсы)

## Технологии

- Python 3.8+
- Tkinter 
- sqlite3 
- urllib + json 
- pytest 
- Black 

## Как запустить

```bash
git clone https://github.com/siiiixxxx/currency-converter-with-tests.git
cd currency-converter-with-tests

python -m venv venv
source venv/bin/activate

python main.py