import telebot
from config import currency_map, TOKEN
from extensions import Validator, Converter, ConvertionException


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
  for key, value in currency_map.items():
    text = '\n'.join((text, f'{key} ({value})'))
  bot.reply_to(message, text)

@bot.message_handler(content_types=['text'])
def convert(message: telebot.types.Message):
  values = message.text.split(' ')

  try:
    quote, base, amount = Validator.validate(values)
    price = Converter.get_price(quote, base, amount)
  except ConvertionException as e:
    bot.reply_to(message, f'Ошибка пользователя.\n{e}')
  except Exception as e:
    bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
  else:
    text = f'Цена {amount} {quote} в {base} = {"{0:.2f}".format(price)}'
    bot.send_message(message.chat.id, text)

bot.polling()