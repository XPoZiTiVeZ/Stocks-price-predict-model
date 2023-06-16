# parser by @aurrog

import apimoex
import requests
import datetime
import pandas as pd
import math
import os
from config import ticker_list
# Импорт всех необходимых библиотек. Apimoex - api МосБиржи


def clean_old_file():
    for ticker in ticker_list:
        data_path = rf'./data/{ticker}_data.csv'
        photo_path = rf'./plots/{ticker}_plot.png'
        MQ_photo_path = rf'./mq_plots/MQ_{ticker}_plot.png'
        try:
            os.remove(data_path)
            os.remove(photo_path)
            os.remove(MQ_photo_path)
        except:
            pass

def parse():
    clean_old_file()
    with requests.Session() as session:
        '''
        Объявление сеанса requests в качестве контекстного менеджера.
        Это гарантирует, что сеанс будет закрыт сразу же после выхода из блока with, даже если произошли необработанные исключения.
        '''
        for ticker in ticker_list:
            # Итерация списка тикеров
            data = pd.DataFrame(apimoex.get_board_history(session,
                                                        ticker, start='2013-01-01', end=str(datetime.date.today()),
                                                        board='TQBR'))
            '''
            Получение истории по бумаге на рынке в указанном режиме торгов за указанный интервал дат и преобразование в pandas Dataframe.
            session - Сессия интернет-соединения
            ticker - Тикер ценной бумаги
            start - Дата начала записи
            end - Дата конца записи
            board - Режим торгов 
            '''
            file_name = ticker + '_data.csv'
            # Создание названия будущего файла
            for index, element in enumerate(data['CLOSE']):
                # Проверка на пропуски в строках данных путем итерации столбца Dataframe
                if math.isnan(element):
                    # Проверка на значение Nan
                    data = data.drop(labels=[index])
                    # Удаление строки с пропуском

            data.to_csv(os.path.join(r'./data/', file_name), index=False)
            # Сохранение файла в .csv формат


if __name__ == "__main__":
    clean_old_file()
    parse()
