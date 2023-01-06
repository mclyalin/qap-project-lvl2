import requests
import json
from config import currency_map

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

    if quote not in currency_map:
      raise ConvertionException(f'Неудалось обработать валюту {quote}')

    if base not in currency_map:
      raise ConvertionException(f'Неудалось обработать валюту {base}')

    quote_ticker, base_ticker = currency_map[quote], currency_map[base]

    try:
      amount = float(amount)
    except ValueError:
      raise ConvertionException(f'Неудалось обработать количество {amount}')

    if amount < 0:
        raise ConvertionException(f'Количество не может быть отрицательным')

    if amount == 0:
        raise ConvertionException(f'Количество не может быть равным 0')

    return quote_ticker, base_ticker, amount