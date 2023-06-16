# bot by @igorar666 and @MSigutin


TOKEN = "5988974979:AAEJWIb4WqFhFoBPvwVS-MfsrlAm4HI_QNQ"

import os.path as pth
from datetime import datetime

import telebot  # Тг бот
from telebot import types  # Для клавиатуры в тг

import posrednik
from model import get_round_num, get_lot_info
from visual import getplot

bot = telebot.TeleBot(TOKEN)  # создание бота
helper = posrednik.Posrednik()

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
    bot.delete_message(message.chat.id, message.id - 2)


@bot.message_handler(commands=["predicts"])
def get_predicts(message):
    markup_inline = types.InlineKeyboardMarkup(row_width=2)

    markup_inline.add(types.InlineKeyboardButton(text=f"Сбербанк (SBER)", callback_data=f"SBER"),
                      types.InlineKeyboardButton(text=f"Газпром (GAZP)", callback_data=f"GAZP"))
    markup_inline.add(types.InlineKeyboardButton(text=f"ОГК-2 (OGKB)", callback_data=f"OGKB"),
                      types.InlineKeyboardButton(text=f"X5 Group (FIVE)", callback_data=f"FIVE"))
    markup_inline.add(types.InlineKeyboardButton(text=f"НОВАТЭК (NVTK)", callback_data=f"NVTK"),
                      types.InlineKeyboardButton(text=f"ПИК (PIKK)", callback_data=f"PIKK"))
    markup_inline.add(types.InlineKeyboardButton(text=f"Роснефть (ROSN)", callback_data=f"ROSN"),
                      types.InlineKeyboardButton(text=f"Интер-PAO (IRAO)", callback_data=f"IRAO"))
    markup_inline.add(types.InlineKeyboardButton(text=f"Яндекс (YNDX)", callback_data=f"YNDX"),
                      types.InlineKeyboardButton(text=f"VK-гдр (VKCO)", callback_data=f"VKCO"))
    markup_inline.add(types.InlineKeyboardButton(text=f"ВТБ (VTBR)", callback_data=f"VTBR"),
                      types.InlineKeyboardButton(text=f"Мечел (MTLR)", callback_data=f"MTLR"))
    markup_inline.add(types.InlineKeyboardButton(text=f"Все акции", callback_data=f"all"))

    bot.send_photo(message.chat.id, open("photo.png", 'rb'), f"Выбери акцию, для которой хочешь получить прогноз",
                   reply_markup=markup_inline)


murkup_MQ = types.InlineKeyboardMarkup()

murkup_MQ.add(types.InlineKeyboardButton(text=f"Получить график в высоком разрешении",
                                         callback_data=f"get_MQ"))
save_stock = ''


@bot.callback_query_handler(func=lambda call: True)
def inline_answer(call):
    global save_stock
    stock = call.data
    stok_predict = 0

    if call.data == "SBER":
        stok_predict = helper.predicted_SBER
        save_stock = "SBER"

    if call.data == "GAZP":
        stok_predict = helper.predicted_GAZP
        save_stock = "GAZP"

    if call.data == "OGKB":
        stok_predict = helper.predicted_OGKB
        save_stock = "OGKB"

    if call.data == "FIVE":
        stok_predict = helper.predicted_FIVE
        save_stock = "FIVE"

    if call.data == "NVTK":
        stok_predict = helper.predicted_NVTK
        save_stock = "NVTK"

    if call.data == "PIKK":
        stok_predict = helper.predicted_PIKK
        save_stock = "PIKK"

    if call.data == "ROSN":
        stok_predict = helper.predicted_ROSN
        save_stock = "ROSN"

    if call.data == "IRAO":
        stok_predict = helper.predicted_IRAO
        save_stock = "IRAO"

    if call.data == "YNDX":
        stok_predict = helper.predicted_YNDX
        save_stock = "YNDX"

    if call.data == "VKCO":
        stok_predict = helper.predicted_VKCO
        save_stock = "VKCO"

    if call.data == "VTBR":
        stok_predict = helper.predicted_VTBR
        save_stock = "VTBR"

    if call.data == "MTLR":
        stok_predict = helper.predicted_MTLR
        save_stock = "MTLR"

    if call.data == "get_MQ":
        bot.send_document(call.message.chat.id, open(rf'MQ_{save_stock}_plot.png', 'rb'),
                          caption=f'{save_stock} stock price')
        
    if call.data == "all":
        papers = ['SBER', 'GAZP', 'OGKB', 'FIVE', 'NVTK', 'PIKK',
                  'ROSN', 'IRAO', 'YNDX', 'VKCO', 'VTBR', 'MTLR']
        # papers = ['SBER', 'GAZP'] # ТЕСТ!!!!
        stok_predicts = {
            'SBER': helper.predicted_SBER,
            'GAZP': helper.predicted_GAZP,
            'OGKB': helper.predicted_OGKB,
            'FIVE': helper.predicted_FIVE,
            'NVTK': helper.predicted_NVTK,
            'PIKK': helper.predicted_PIKK,
            'ROSN': helper.predicted_ROSN,
            'IRAO': helper.predicted_IRAO,
            'YNDX': helper.predicted_YNDX,
            'VKCO': helper.predicted_VKCO,
            'VTBR': helper.predicted_VTBR,
            'MTLR': helper.predicted_MTLR
        }
        for paper in papers:
            print(paper)

            open_file = open(f'data/{paper}_data.csv', 'rb')
            last_date = '.'.join((str(open_file.readlines()[-1]).split(',')[1]).split('-')[::-1])
            open_file.close()

            open_file = open(f'data/{paper}_data.csv', 'rb')
            last_price = float(str(open_file.readlines()[-1]).split(',')[2])
            open_file.close()

            delta_price = round(abs(stok_predicts[paper] - last_price), get_round_num(paper))
            profit = round(delta_price * get_lot_info(paper), get_round_num(paper) + len(str(get_lot_info(paper))) - 1)
            if last_price < stok_predicts[paper]:
                bot.send_photo(call.message.chat.id,
                               open(f"data/{paper}_plot.png", "rb"),
                               f"Прогноз от _{last_date}_:\n\nАкции *{paper}* вырастут на {delta_price} до *{stok_predicts[paper]}* ₽▲\n\nПотенциальная прибыль от _ПОКУПКИ_ одной акции составит *{profit}* ₽",
                )

            else:
                bot.send_photo(call.message.chat.id,
                               open(f"data/{paper}_plot.png", "rb"),
                               f"Прогноз от _{last_date}_:\n\nАкции *{paper}* упадут на {delta_price} до *{stok_predicts[paper]}* ₽▼\n\nПотенциальная прибыль от _ПРОДАЖИ_ одной акции с её выкупом в дальнейшем составит *{profit}* ₽",
                )

            if not pth.isfile(f'data/MQ_{paper}_plot.png'):
                getplot(paper, f'data/{paper}_data.csv', stok_predicts[paper],
                    max_quality=True)
                print('create MQ photo')

    if call.data != 'get_MQ' and call.data != 'all':
        open_file = open(f'data/{call.data}_data.csv', 'rb')
        last_date = '.'.join((str(open_file.readlines()[-1]).split(',')[1]).split('-')[::-1])
        open_file.close()

        open_file = open(f'data/{call.data}_data.csv', 'rb')
        last_price = float(str(open_file.readlines()[-1]).split(',')[2])
        open_file.close()

        delta_price = round(abs(stok_predict - last_price), get_round_num(stock))
        profit = round(delta_price * get_lot_info(stock), get_round_num(stock) + len(str(get_lot_info(stock))) - 1)
        if last_price < stok_predict:
            bot.edit_message_media(media=types.InputMediaPhoto(open(f"data/{stock}_plot.png", "rb"),
                                                               caption=f"Прогноз от _{last_date}_:\n\nАкции *{stock}* вырастут на {delta_price} до *{stok_predict}* ₽▲\n\nПотенциальная прибыль от _ПОКУПКИ_ одной акции составит *{profit}* ₽",
                                                               parse_mode='Markdown'),
                                   chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=murkup_MQ)
        else:
            bot.edit_message_media(media=types.InputMediaPhoto(open(f"data/{stock}_plot.png", "rb"),
                                                               caption=f"Прогноз от _{last_date}_:\n\nАкции *{stock}* упадут на {delta_price} до *{stok_predict}* ₽▼\n\nПотенциальная прибыль от _ПРОДАЖИ_ одной акции с её выкупом в дальнейшем составит *{profit}* ₽",
                                                               parse_mode='Markdown'),
                                   chat_id=call.message.chat.id, message_id=call.message.id, reply_markup=murkup_MQ)
        if not pth.isfile(f'data/MQ_{stock}_plot.png'):
            getplot(stock, f'data/{stock}_data.csv', stok_predict,
                    max_quality=True)
            print('create MQ photo')


@bot.message_handler(content_types=['text'])
def default_message(message):  # обработчик сообщений вместо команд
    if message.text == "Прогноз цены на ближайшие дни":
        get_predicts(message)
    elif message.text == 'Обновить данные':
        reload(message)


print("Бот запущен")
helper.main()
bot.polling(none_stop=True, interval=0, skip_pending=True)  # запуск бота
