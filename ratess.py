import requests

def get_currency_rates(base_currency):
    api_url = f"https://api.exchangerate-api.com/v4/latest/{base_currency}"
    response = requests.get(api_url)
    return response.json()["rates"]

def get_wanted_currency(from_currency, to_currency, amount):
    rates = get_currency_rates(from_currency)
    return rates[to_currency]*amount