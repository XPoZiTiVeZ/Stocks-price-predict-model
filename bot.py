# bot by @igorar666 and @MSigutin
import telebot  # Тг бот
from telebot import types  # Для клавиатуры в тг
import posrednik
import websource
from model import get_round_num
from visual import getplot_image
from datetime import datetime
from config import BOT_token, ticker_info, data_path, predict_data_path, plots_path, mq_plots_path, localhost


bot = telebot.TeleBot(BOT_token)  # создание бота
helper = posrednik.Posrednik()
murkup_MQ = ''
    

'''У нас есть код на Python-e который состоит из нескольких частей:
1. Парсер. Он получает новейшие данные об акциях
2. Нейросеть. Каждый раз она переобучается на данных и делает прогноз на завтра
3. Визуализатор. Делает график из последних данных в таблице и прогноза
4. Бот. С ним вы общаетесь в Телеграме
5. Посредник. Связующее звену между все вышестоящим'''


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


@bot.message_handler(commands=["predicts"])
def get_predicts(message):
    markup_inline = types.InlineKeyboardMarkup(row_width=2)
    
    buttons = [types.InlineKeyboardButton(text=f"{ticker_info.get(ticker)[1]} ({ticker})", callback_data=f"{ticker}") for ticker in ticker_info.keys()]
    markup_inline.add(*buttons)
    markup_inline.add(types.InlineKeyboardButton(text=f"Выбрать все акции", callback_data=f"all"))
    
    bot.send_photo(message.chat.id, open("photo.png", 'rb'), f"Выбери акцию, для которой хочешь получить прогноз",
                   reply_markup=markup_inline)


def send_predict(message, stock: str, stock_predict: float, link, series=False):
    murkup_MQ = types.InlineKeyboardMarkup()
    murkup_MQ.add(types.InlineKeyboardButton(text=f"Открыть динамический график", url=f'{link}/plots/{stock}'))
    murkup_MQ.add(types.InlineKeyboardButton(text=f"Скачать график в высоком разрешении", callback_data=f"get_MQ_{stock}"))
    murkup_MQ.add(types.InlineKeyboardButton(text=f"На главную", callback_data=f"on_main"))
    
    open_file = open(data_path(stock), 'rb')
    last_date = '.'.join((str(open_file.readlines()[-1]).split(',')[1]).split('-')[::-1])
    open_file.close()

    open_file = open(data_path(stock), 'rb')
    last_price = float(str(open_file.readlines()[-1]).split(',')[2])
    open_file.close()

    delta_price = round(abs(stock_predict - last_price), get_round_num(stock))
    profit = round(delta_price * ticker_info.get(stock)[0], get_round_num(stock) + len(str(ticker_info.get(stock)[0])) - 1)
    
    photo = open(plots_path(stock), "rb")
    caption_predict_up = f"Прогноз от _{last_date}_:\n\nАкции *{stock}* вырастут до *{stock_predict}* ₽▲\n\nПотенциальная прибыль от _ПОКУПКИ_ или _УДЕРЖАНИЯ_ одной акции составит *{profit}* ₽"
    caption_predict_down = f"Прогноз от _{last_date}_:\n\nАкции *{stock}* упадут до *{stock_predict}* ₽▼\n\nПотенциальная прибыль от _ПРОДАЖИ_ одной акции с её выкупом в дальнейшем составит *{profit}* ₽"
    
    if series:
        if last_price < stock_predict:
            bot.send_photo(photo=photo, caption=caption_predict_up, parse_mode='Markdown', chat_id=message.chat.id, reply_markup=murkup_MQ)
        else:
            bot.send_photo(photo=photo, caption=caption_predict_down, parse_mode='Markdown', chat_id=message.chat.id, reply_markup=murkup_MQ)
    else:
        if last_price < stock_predict:
            bot.edit_message_media(media=types.InputMediaPhoto(photo, caption=caption_predict_up, parse_mode='Markdown'),
                                   chat_id=message.chat.id, message_id=message.id, reply_markup=murkup_MQ)
        else:
            bot.edit_message_media(media=types.InputMediaPhoto(photo, caption=caption_predict_down, parse_mode='Markdown'),
                                   chat_id=message.chat.id, message_id=message.id, reply_markup=murkup_MQ)


@bot.callback_query_handler(func=lambda call: True)
def inline_answer(call):
    try:
        link = str(ngrok.get_tunnels()).split('"')[1][6:] if localhost else '127.0.0.1'
    except:
        link = '127.0.0.1'

    if call.data in ticker_info.keys():
        stock_predict = float((str(open(predict_data_path(call.data), 'rb').readlines()[-1]).split(',')[2])[:-6])
        try:
            send_predict(call.message, call.data, stock_predict, link)
        except:
            getplot_image(call.data, data_path(call.data), predict_data_path(call.data), max_quality=True)
            send_predict(call.message, call.data, stock_predict, link)

    elif "get_MQ_" in call.data:
        try:
            bot.send_document(call.message.chat.id, open(mq_plots_path(call.data[-4:]), 'rb'), caption=f'{call.data[-4:]} stock price')
        except:
            getplot_image(call.data[-4:], data_path(call.data[-4:]), predict_data_path(call.data[-4:]), max_quality=True)
            bot.send_document(call.message.chat.id, open(mq_plots_path(call.data[-4:]), 'rb'), caption=f'{call.data[-4:]} stock price')

    elif call.data == 'all':
        for ticker in ticker_info.keys():
            stock_predict = float((str(open(predict_data_path(ticker), 'rb').readlines()[-1]).split(',')[2])[:-6])
            send_predict(call.message, ticker, stock_predict, link, series=True)

    elif call.data == 'on_main':
        bot.delete_message(call.message.chat.id, call.message.id)
        get_predicts(call.message)
    
    else:
        pass


@bot.message_handler(content_types=['text'])
def default_message(message):  # обработчик сообщений вместо команд
    if message.text == "Прогноз цены на ближайшие дни":
        get_predicts(message)
    elif message.text == 'Обновить данные':
        reload(message)


print("Бот запущен")
websource.start()
if localhost:
    import hosting
    from pyngrok import ngrok
    hosting.start()
helper.main()
bot.polling(none_stop=True, interval=0, skip_pending=True)  # запуск бота
