import requests
import json
from config import keys

class ConvertionException(Exception):
  pass

class Converter:
  @staticmethod
  def get_price(quote: str, base: str, amount: float):
    r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={quote}&tsyms={base}')
    rate = json.loads(r.content)[base]
    price = amount * float(rate)

    return price

class Validator:
  @staticmethod
  def validate(values: list):
    if len(values) != 3:
      raise ConvertionException('Неверное количество параметров')

    quote, base, amount = values

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

    return quote_ticker, base_ticker, amount