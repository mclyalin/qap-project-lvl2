import requests
import json
from config import keys

class ConvertionException(Exception):
  pass

class Converter:
  @staticmethod
  def convert(quote: str, base: str, amount: str):
    if quote == base:
      raise ConvertionException(f'Невозможно перевести {quote} в {base}')

    if quote not in keys:
      raise ConvertionException(f'Неудалось обработать валюту {quote}')

    if base not in keys:
      raise ConvertionException(f'Неудалось обработать валюту {base}')

    quote_ticker, base_ticker = keys[quote], keys[base]

    try:
      amount = float(amount)
    except ValueError:
      raise ConvertionException(f'Неудалось обработать количество {amount}')

    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote_ticker}&tsyms={base_ticker}')
    rate = int(json.loads(r.content)[keys[base]])
    total_base = amount * rate

    return quote_ticker, base_ticker, total_base