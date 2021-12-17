import telebot
from config import TOKEN, keys
from utils import ConvertException, CryptoConverter

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['help'])
def start(message: telebot.types.Message):
    text = 'В данном боте вы сможете конвертировать 1 криптовалюту в другую, а также перевести её в USD или RUB.' \
           'Нажмите /start чтобы конвертировать валюту. Нажмите /commands чтобы увидеть список валют.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['start'])
def start(message: telebot.types.Message):
    text = 'Чтобы начать введите ваш запрос в следуюзем формате: ' \
           'Валюта которую хотите конвертирвать Валюта в которую хотите ковертировать Сумма' \
           'Разделитель - пробел.'
    bot.reply_to(message, text)


@bot.message_handler(commands=['commands'])
def start(message: telebot.types.Message):
    text = 'Доступные валюты:'
    for value in keys.values():
        text = '\n'.join((text, value,))
    bot.reply_to(message, text)


@bot.message_handler(content_types=['text'])
def start(message: telebot.types.Message):
    try:
        values = message.text.split(' ')

        if len(values) != 3:
            raise ConvertException('Кол-во парметров отлично от 3.')

        quote, base, amount = values
        total_base = CryptoConverter.convert(quote, base, amount)
    except ConvertException as e:
        bot.reply_to(message, f'Ошибка пользователя.\n{e}')
    except Exception as e:
        bot.reply_to(message, f'Не удалось обработать команду\n{e}')
    else:
        text = f'Стоимость {amount} {quote} составит {total_base} {keys[base]}.'
        bot.send_message(message.chat.id, text)


bot.polling()
