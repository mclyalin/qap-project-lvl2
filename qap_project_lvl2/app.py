import telebot
from config import keys, TOKEN
from utils import Converter, ConvertionException


bot = telebot.TeleBot(TOKEN)

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