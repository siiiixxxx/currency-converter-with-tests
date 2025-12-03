import tkinter as tk
from tkinter import ttk, messagebox
from api import fetch_rates
from db import init_db


class CurrencyConverterApp(tk.Tk):
    def __init__(self):
        super().__init__()
        self.title("Калькулятор кредита с конвертацией")
        self.geometry("500x700")
        self.resizable(False, False)

        init_db()
        self.rates = {}
        self.target_var = tk.StringVar(value="USD")

        self.create_widgets()

        self.after(100, self.update_db)

    def create_widgets(self):
        pad = {'padx': 10, 'pady': 5}

        tk.Label(self, text="Сумма кредита (₽):").grid(row=0, column=0, sticky='w', **pad)
        self.loan_var = tk.StringVar()
        tk.Entry(self, textvariable=self.loan_var).grid(row=0, column=1, sticky='ew', **pad)

        tk.Label(self, text="Срок кредита (мес):").grid(row=1, column=0, sticky='w', **pad)
        self.time_var = tk.StringVar()
        tk.Entry(self, textvariable=self.time_var).grid(row=1, column=1, sticky='ew', **pad)

        tk.Label(self, text="Годовая ставка (%):").grid(row=2, column=0, sticky='w', **pad)
        self.interest_var = tk.StringVar()
        tk.Entry(self, textvariable=self.interest_var).grid(row=2, column=1, sticky='ew', **pad)

        tk.Button(self, text="Рассчитать кредит", command=self.calculate_loan).grid(row=3, column=0, columnspan=2, pady=15)

        tk.Label(self, text="Ежемесячный платёж (₽):").grid(row=4, column=0, sticky='w', **pad)
        self.monthly_label = tk.Label(self, text="", font=("Arial", 12, "bold"))
        self.monthly_label.grid(row=4, column=1, sticky='w', **pad)

        tk.Label(self, text="Сумма к выплате (₽):").grid(row=5, column=0, sticky='w', **pad)
        self.loan_sum_label = tk.Label(self, text="")
        self.loan_sum_label.grid(row=5, column=1, sticky='w', **pad)

        tk.Label(self, text="Переплата (₽):").grid(row=6, column=0, sticky='w', **pad)
        self.interest_label = tk.Label(self, text="")
        self.interest_label.grid(row=6, column=1, sticky='w', **pad)

        tk.Label(self, text="Конвертировать в:").grid(row=7, column=0, sticky='w', **pad)
        currencies = ["USD", "EUR", "CNY", "GBP"]
        ttk.Combobox(self, textvariable=self.target_var, values=currencies, state="readonly").grid(row=7, column=1, sticky='ew', **pad)

        tk.Button(self, text="Конвертировать", command=self.convert).grid(row=8, column=0, columnspan=2, pady=10)

        self.result_label = tk.Label(self, text="", font=("Arial", 14, "bold"), fg="green")
        self.result_label.grid(row=9, column=0, columnspan=2, pady=10)

        tk.Button(self, text="Обновить курсы", command=self.update_db).grid(row=10, column=0, columnspan=2, pady=5)

        self.log_text = tk.Text(self, height=6, state='disabled', wrap='word')
        self.log_text.grid(row=11, column=0, columnspan=2, sticky='ew', padx=10, pady=10)
        self.log_text.grid_rowconfigure(0, weight=1)

        self.grid_columnconfigure(1, weight=1)

    def log(self, message: str):
        self.log_text.config(state='normal')
        self.log_text.insert('end', f"{message}\n")
        self.log_text.see('end')
        self.log_text.config(state='disabled')

    def is_loan_invalid(self, value: float, message: str) -> bool:
        if value <= 0:
            messagebox.showerror("Ошибка", message)
            self.log(f"Ошибка: {message}")
            return True
        return False

    def calculate_loan(self):
        try:
            loan = float(self.loan_var.get())
            months = int(self.time_var.get())
            annual_rate = float(self.interest_var.get()) / 100

            if self.is_loan_invalid(loan, "Сумма кредита должна быть > 0"):
                return
            if self.is_loan_invalid(months, "Срок должен быть > 0"):
                return
            if self.is_loan_invalid(annual_rate, "Ставка должна быть > 0"):
                return

            monthly_rate = annual_rate / 12
            if monthly_rate == 0:
                payment = loan / months
            else:
                payment = loan * (monthly_rate * (1 + monthly_rate) ** months) / ((1 + monthly_rate) ** months - 1)

            total = payment * months
            overpayment = total - loan

            self.monthly_label.config(text=f"{payment:,.2f} ₽")
            self.loan_sum_label.config(text=f"{total:,.2f} ₽")
            self.interest_label.config(text=f"{overpayment:,.2f} ₽")

            self.log(f"Расчёт: {loan:,.0f} ₽ → {payment:,.2f} ₽/мес")

        except ValueError:
            messagebox.showerror("Ошибка", "Введите корректные числа")
            self.log("Ошибка ввода")

    def convert(self):
        try:
            monthly_rub = float(self.monthly_label.cget("text").replace(" ₽", "").replace(",", ""))
            target = self.target_var.get()
            rate = self.rates.get(target, 0)

            if rate == 0:
                self.result_label.config(text="Курс недоступен")
                self.log("Конвертация: курс не загружен")
                return

            converted = monthly_rub / rate
            self.result_label.config(text=f"{converted:,.2f} {target}")
            self.log(f"Конвертация: {monthly_rub:,.0f} ₽ → {converted:,.2f} {target}")

        except:
                self.result_label.config(text="Сначала рассчитайте платёж")

    def update_db(self):
        self.log("Загрузка курсов...")
        self.rates = fetch_rates()
        self.log(f"Курсы обновлены: {', '.join([f'{k}: {v}' for k, v in self.rates.items()])}")

if __name__ == "__main__":
            app = CurrencyConverterApp()
            app.mainloop()