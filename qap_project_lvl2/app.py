import telebot
import requests
import json


TOKEN = '5706684762:AAGakWlavDMV8Af-2jKT8sZbHwVtlZMvaZY'

bot = telebot.TeleBot(TOKEN)

keys = {
  'биткоин': 'BTC',
  'эфириум': 'ETH',
  'доллар': 'USD'
}

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



@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
  text = 'Введите комманду в следующем формате:\n \
<из какой валюты> <в какую валюту> <сколько перевести>\n \
Например: доллар евро 100\n \
/values - список всех доступных валют'
  bot.reply_to(message, text)

@bot.message_handler(commands=['values'])
def values(message: telebot.types.Message):
  text = 'Доступные валюты:'
  for key in keys.keys():
    text = '\n'.join((text, key, ))
  bot.reply_to(message, text)

@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
  values = message.text.split(' ')

  if len(values) != 3:
    raise ConvertionException('Неверное количество параметров')

  quote, base, amount = values
  quote_ticker, base_ticker, total_base = Converter.convert(quote, base, amount)
  ##
  text = f'Цена {amount} {quote_ticker} в {base_ticker} = {total_base}'
  bot.send_message(message.chat.id, text)

bot.polling()