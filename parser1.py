# parser by @aurrog

import apimoex
import requests
import datetime
import pandas as pd
import math
import os
from config import ticker_info, data_path, predict_data_path, plots_path, mq_plots_path
# Импорт всех необходимых библиотек. Apimoex - api МосБиржи


def clean_old_file():
    for ticker in ticker_info.keys():
        try:
            os.remove(data_path(ticker))
            os.remove(plots_path(ticker))
            os.remove(mq_plots_path(ticker))
        except Exception as e:
            print(e)


def parse():
    clean_old_file()
    with requests.Session() as session:
        '''
        Объявление сеанса requests в качестве контекстного менеджера.
        Это гарантирует, что сеанс будет закрыт сразу же после выхода из блока with, даже если произошли необработанные исключения.
        '''
        for ticker in ticker_info.keys():
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
            # Создание названия будущего файла
            for index, element in enumerate(data['CLOSE']):
                # Проверка на пропуски в строках данных путем итерации столбца Dataframe
                if math.isnan(element):
                    # Проверка на значение Nan
                    data = data.drop(labels=[index])
                    # Удаление строки с пропуском

            data.to_csv(os.path.join(data_path(ticker)), index=False)
            # Сохранение файла в .csv формат


if __name__ == "__main__":
    clean_old_file()
    parse()
