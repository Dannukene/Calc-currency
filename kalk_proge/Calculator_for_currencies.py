import tkinter as tk
from tkinter import ttk, messagebox, scrolledtext
import requests
import pycountry

# List of additional currencies
additional_currencies = {
    "AED": "UAE Dirham", "AFN": "Afghani", "ALL": "Lek", "AMD": "Armenian Dram",
    "ANG": "Netherlands Antillean Guilder", "AOA": "Kwanza", "ARS": "Argentine Peso",
    "AUD": "Australian Dollar", "AWG": "Aruban Florin", "AZN": "Azerbaijan Manat",
    "BAM": "Convertible Mark", "BBD": "Barbados Dollar", "BDT": "Taka",
    "BGN": "Bulgarian Lev", "BHD": "Bahraini Dinar", "BIF": "Burundi Franc",
    "BMD": "Bermudian Dollar", "BND": "Brunei Dollar", "BOB": "Boliviano",
    "BRL": "Brazilian Real", "BSD": "Bahamian Dollar", "BTN": "Ngultrum",
    "CAD": "Canadian Dollar", "CDF": "Congolese Franc", "CHF": "Swiss Franc",
    "CNY": "Yuan Renminbi", "COP": "Colombian Peso", "CRC": "Costa Rican Colon",
    "CZK": "Czech Koruna", "DKK": "Danish Krone", "DOP": "Dominican Peso",
    "EGP": "Egyptian Pound", "EUR": "Euro", "GBP": "Pound Sterling",
    "INR": "Indian Rupee", "JPY": "Yen", "KES": "Kenyan Shilling",
    "KRW": "Won", "KWD": "Kuwaiti Dinar", "MZN": "Mozambique Metical",
    "NOK": "Norwegian Krone", "NZD": "New Zealand Dollar", "OMR": "Rial Omani",
    "PHP": "Philippine Peso", "PKR": "Pakistan Rupee", "PLN": "Zloty",
    "QAR": "Qatari Rial", "RON": "Romanian Leu", "RUB": "Russian Ruble",
    "SAR": "Saudi Riyal", "SEK": "Swedish Krona", "SGD": "Singapore Dollar",
    "THB": "Baht", "TRY": "Turkish Lira", "USD": "US Dollar", "ZAR": "Rand"
}

def get_currency_code(currency_name_or_code):
    currency_name_or_code = currency_name_or_code.strip().upper()
    valid_currencies = {c.alpha_3 for c in pycountry.currencies}
    if currency_name_or_code in valid_currencies:
        return currency_name_or_code
    for currency in pycountry.currencies:
        if currency.name.lower() == currency_name_or_code.lower():
            return currency.alpha_3
    return None

def get_exchange_rate(api_key, base_currency):
    url = f'https://v6.exchangerate-api.com/v6/{api_key}/latest/{base_currency}'
    try:
        response = requests.get(url)
        response.raise_for_status()
        data = response.json()
        if data.get("result") == "success":
            return data["conversion_rates"]
        else:
            messagebox.showerror("Error", f"Error fetching exchange rates: {data.get('error-type', 'Unknown error')}")
            return None
    except requests.exceptions.RequestException as e:
        messagebox.showerror("Error", f"Network error: {e}")
        return None

def convert_currency(amount, from_currency, to_currency, rates):
    if to_currency in rates:
        return amount * rates[to_currency]
    else:
        messagebox.showerror("Error", f"Currency '{to_currency}' not supported by the API.")
        return None

def convert_button_click():
    api_key = "51f8e48f58a834866c7d749d"
    base_currency = get_currency_code(base_currency_entry.get())
    target_currency = get_currency_code(target_currency_entry.get())
    try:
        amount = float(amount_entry.get())
    except ValueError:
        messagebox.showerror("Error", "Invalid amount. Please enter a numeric value.")
        return
    if not base_currency or not target_currency:
        messagebox.showerror("Error", "Invalid currency codes.")
        return
    rates = get_exchange_rate(api_key, base_currency)
    if rates and target_currency in rates:
        converted_amount = convert_currency(amount, base_currency, target_currency, rates)
        if converted_amount is not None:
            result_label.config(text=f"{amount} {base_currency} = {converted_amount:.2f} {target_currency}")
    else:
        messagebox.showerror("Error", f"Exchange rate for {target_currency} not available.")

def populate_country_list():
    country_currency_list.delete(1.0, tk.END)
    search_term = search_entry.get().lower()
    for country in pycountry.countries:
        try:
            currency = pycountry.currencies.lookup(country.alpha_3)
            if search_term in country.name.lower() or search_term in currency.name.lower():
                country_currency_list.insert(tk.END, f"{country.name} - {currency.name} ({currency.alpha_3})\n")
        except LookupError:
            pass
    for code, name in additional_currencies.items():
        if search_term in name.lower() or search_term in code.lower():
            country_currency_list.insert(tk.END, f"{code} - {name}\n")

window = tk.Tk()
window.title("Currency Converter")

converter_frame = ttk.Frame(window)
converter_frame.grid(row=0, column=0, padx=10, pady=10)

ttk.Label(converter_frame, text="Base Currency:").grid(row=0, column=0, padx=5, pady=5)
base_currency_entry = ttk.Entry(converter_frame)
base_currency_entry.grid(row=0, column=1, padx=5, pady=5)

ttk.Label(converter_frame, text="Target Currency:").grid(row=1, column=0, padx=5, pady=5)
target_currency_entry = ttk.Entry(converter_frame)
target_currency_entry.grid(row=1, column=1, padx=5, pady=5)

ttk.Label(converter_frame, text="Amount:").grid(row=2, column=0, padx=5, pady=5)
amount_entry = ttk.Entry(converter_frame)
amount_entry.grid(row=2, column=1, padx=5, pady=5)

convert_button = ttk.Button(converter_frame, text="Convert", command=convert_button_click)
convert_button.grid(row=3, column=0, columnspan=2, pady=10)

result_label = ttk.Label(converter_frame, text="")
result_label.grid(row=4, column=0, columnspan=2)

country_list_frame = ttk.Frame(window)
country_list_frame.grid(row=0, column=1, padx=10, pady=10)

ttk.Label(country_list_frame, text="Search:").grid(row=0, column=0, padx=5, pady=5)
search_entry = ttk.Entry(country_list_frame)
search_entry.grid(row=0, column=1, padx=5, pady=5)
search_entry.bind("<KeyRelease>", lambda event: populate_country_list())

country_currency_list = scrolledtext.ScrolledText(country_list_frame, width=40, height=20)
country_currency_list.grid(row=1, column=0, columnspan=2, padx=5, pady=5)

populate_country_list()
window.mainloop()
