import telebot

from settings import TOKEN, СurrenciesValues
from exception import ConvertionException, ApiServiceError
from extensions import CurrencyConvertor, InflectCurrency

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', 'help'])
def help(message: telebot.types.Message):
    text = """Чтобы начать работу введите команду боту в следующем формате: 
<имя валюты, цену которой нужно узнать> <имя валюты, в которой надо узнать цену первой валюты>
 <количество первой валюты>.\n
Для получения списка доступных валют введите команду /values"""
    bot.reply_to(message, text)


@bot.message_handler(commands=['values'])
def show_currency_list(message: telebot.types.Message):
    text = 'Доступные валюты:\n'
    for currency_type in СurrenciesValues:
        text += f"- {currency_type.value}\n"
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text', ])
def convert(message: telebot.types.Message):
    values = list(map(lambda x: x.lower(), message.text.split(' ')))
    try:
        if len(values) != 3:
            raise ConvertionException('Неверное количество параметров.')
        base, quote, amount = values
        price = CurrencyConvertor.get_price(base=base, quote=quote, amount=amount)
    except ConvertionException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except ApiServiceError as e:
        bot.reply_to(message, f'Ошибка сервиса.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду.\n{e}')
    else:
        txt = (f'{amount} {InflectCurrency.make_agree_with_amount(amount=float(amount), values=base)} '
               f'равно {price} {InflectCurrency.make_agree_with_amount(amount=price, values=quote)}.')

        bot.send_message(message.chat.id, txt)


bot.polling()