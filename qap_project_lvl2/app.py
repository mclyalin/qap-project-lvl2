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

@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
  text = 'Чтобы начать работу введите комманду в следующем формате:\n \
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
  quote, base, amount = message.text.split(' ')
  r = requests.get(f'https://min-api.cryptocompare.com/data/price?fsym={keys[quote]}&tsyms={keys[base]}')
  total_base = json.loads(r.content)[keys[base]]
  text = f'Цена {amount} {keys[quote]} в {keys[base]} = {total_base}'
  bot.send_message(message.chat.id, text)

bot.polling()