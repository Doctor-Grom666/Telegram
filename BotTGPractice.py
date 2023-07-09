import telebot
from config import keys, TOKEN
from extensions import APIExeption, CryptoConverter


bot = telebot.TeleBot(TOKEN)

@bot.message_handler(commands=['start', 'help'])
def help(message):
    text = 'Чтобы начать работу, введите комманду боту в седующем формате:\n<имя валюты> \
<в какую валюту перевести> \
<количество переводимой валюты>\nУвидеть список доступных валют: /values'
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def values(message):
    text = 'Доступные валюты:'
    for key in keys.keys():
        text = '\n'.join((text, key))
    bot.reply_to(message, text)



@bot.message_handler(content_types=['text'])
def convert(message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise APIExeption(f'Неверное количество параметров.')

        base, quote, amount = values
        total_base = CryptoConverter.get_price(base, quote, amount)
    except APIExeption as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Цена {amount} {base} в {quote} - {total_base}'
        bot.send_message(message.chat.id, text)



bot.polling()