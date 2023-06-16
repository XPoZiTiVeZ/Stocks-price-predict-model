# bot by @igorar666 and @MSigutin

TOKEN = "5910726765:AAH0jbV9TlhctKHMoNBIfxj_5ie0OopZtXw"

import os.path as pth
from datetime import datetime

import telebot  # Тг бот
from telebot import types  # Для клавиатуры в тг

import websource


import posrednik
from model import get_round_num, get_lot_info
from visual import getplot_image
from config import ticker_list

bot = telebot.TeleBot(TOKEN)  # создание бота
helper = posrednik.Posrednik()
localhost = True

if localhost:
    import hosting
    from pyngrok import ngrok
    hosting.start()


'''
У нас есть код на Python-e который состоит из нескольких частей:
1. Парсер. Он получает новейшие данные об акциях
2. Нейросеть. Каждый раз она переобучается на данных и делает прогноз на завтра
3. Визуализатор. Делает график из последних данных в таблице и прогноза
4. Бот. С ним вы общаетесь в Телеграме
5. Посредник. Связующее звену между всем вышестоящим
'''

@bot.message_handler(commands=["start"])
def start(message):  # ответ на команду start
    markup_reply = types.ReplyKeyboardMarkup(resize_keyboard=True, row_width=2)
    item1 = types.KeyboardButton("Прогноз цены на ближайшие дни")
    item2 = types.KeyboardButton("Обновить данные")
    markup_reply.add(item1)
    markup_reply.add(item2)
    bot.send_message(message.chat.id,
                     f"Сразу к делу!\n\n*Нажми кнопку на всплывшей клавиатуре для вывода списка команд*",
                     reply_markup=markup_reply, parse_mode='Markdown')


@bot.message_handler(commands=["reload"])
def reload(message):
    bot.send_message(message.chat.id, "_Обновление данных и перезагрузка..._", parse_mode='Markdown')
    print(
        f'Обновление данных пользователем Телеграм {message.chat.first_name} {message.chat.last_name} - @{message.chat.username}')
    helper.main()
    now = datetime.now()
    date_now = f'{now.day}.{now.month}.{now.year}'
    time_now = f'{now.hour}:{now.minute}:{now.second}'
    bot.send_message(text=f"Данные обновлены {date_now} в {time_now} по МСК", chat_id=message.chat.id)
    bot.delete_message(message.chat.id, message.id - 2)


@bot.message_handler(commands=["predicts"])
def get_predicts(message):
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    buttons = [types.InlineKeyboardButton(text=f"Сбербанк ({ticker})", callback_data=f"{ticker}") for ticker in ticker_list]
    markup_inline.add(*buttons)

    bot.send_photo(message.chat.id, open("photo.png", 'rb'), f"Выбери акцию, для которой хочешь получить прогноз",
                   reply_markup=markup_inline)

@bot.callback_query_handler(func=lambda call: True)
def inline_answer(call):
    stock = call.data
    stock_predict = 0
    murkup_MQ = ''

    if call.data in ticker_list:
        stock_predict = helper.predicted[call.data]
        if localhost:
            link = str(ngrok.get_tunnels()).split('"')[1][6:]
        else:
            link = '127.0.0.1'
        murkup_MQ = types.InlineKeyboardMarkup(row_width=1).add(types.InlineKeyboardButton(text=f"Открыть динамический график", url=f'{link}/plots/{call.data}'),
                                                    types.InlineKeyboardButton(text=f"Получить график в высоком разрешении", callback_data=f"get_MQ_{call.data}"))

    if "get_MQ_" in call.data:
        try:
            bot.send_document(call.message.chat.id, open(rf'./mq_plots/MQ_{call.data[-4:]}_plot.png', 'rb'),
                            caption=f'{call.data[-4:]} stock price')
        except:
            getplot_image(stock, rf'./data/{call.data}_data.csv', rf'./predata/{call.data}_predata.csv', max_quality=True)
            bot.send_document(call.message.chat.id, open(rf'./mq_plots/MQ_{call.data[-4:]}_plot.png', 'rb'), caption=f'{call.data[-4:]} stock price')

    if "get_MQ_" not in call.data:
        open_file = open(f'./data/{call.data}_data.csv', 'rb')
        last_date = '.'.join((str(open_file.readlines()[-1]).split(',')[1]).split('-')[::-1])
        open_file.close()

        open_file = open(f'./data/{call.data}_data.csv', 'rb')
        last_price = float(str(open_file.readlines()[-1]).split(',')[2])
        open_file.close()

        delta_price = round(abs(stock_predict - last_price), get_round_num(stock))
        profit = round(delta_price * get_lot_info(stock), get_round_num(stock) + len(str(get_lot_info(stock))) - 1)
        if last_price < stock_predict:
            bot.edit_message_media(media=types.InputMediaPhoto(open(f"./plots/{stock}_plot.png", "rb"),
                                                               caption=f"Прогноз от _{last_date}_:\n\nАкции *{stock}* вырастут на {delta_price} до *{stock_predict}* ₽▲\n\nПотенциальная прибыль от _ПОКУПКИ_ одной акции составит *{profit}* ₽",
                                                               parse_mode='Markdown'),
                                   chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=murkup_MQ)
        else:
            bot.edit_message_media(media=types.InputMediaPhoto(open(f"./plots/{stock}_plot.png", "rb"),
                                                               caption=f"Прогноз от _{last_date}_:\n\nАкции *{stock}* упадут на {delta_price} до *{stock_predict}* ₽▼\n\nПотенциальная прибыль от _ПРОДАЖИ_ одной акции с её выкупом в дальнейшем составит *{profit}* ₽",
                                                               parse_mode='Markdown'),
                                   chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=murkup_MQ)


@bot.message_handler(content_types=['text'])
def default_message(message):  # обработчик сообщений вместо команд
    if message.text == "Прогноз цены на ближайшие дни":
        get_predicts(message)
    elif message.text == 'Обновить данные':
        reload(message)


print("Бот запущен")
websource.start()
helper.main()
try:
    bot.polling(none_stop=True, interval=0, skip_pending=True)  # запуск бота
except Exception as e:
    print(e)
