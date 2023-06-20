BOT_token = '' # Вставьте свой токен телеграмм бота
NGROK_token = '' # Вставьте свой токен приложения ngrok, если нужно
localhost = False # Если вы планируете использовать ngrok, установите True

data_path = lambda ticker: rf'./data/{ticker}_data.csv'
predict_data_path = lambda ticker: rf'./predict_data/{ticker}_predict_data.csv'
plots_path = lambda ticker: rf'./plots/{ticker}_plot.png'
mq_plots_path = lambda ticker: rf'./mq_plots/MQ_{ticker}_plot.png'

ticker_info = {'SBER':(10, 'Сбербанк'), 
               'GAZP':(1, 'Газпром'), 
               'OGKB':(1000, 'ОГК-2'), 
               'FIVE':(1, 'X5 Group'), 
               'NVTK':(1, 'Новатэк'), 
               'PIKK':(1, 'ГРУППА КОМПАНИЙ ПИК'),
               'ROSN':(1, 'Роснефть'), 
               'IRAO':(100, 'Интер РАО'), 
               'YNDX':(1, 'Яндекс'), 
               'VKCO':(1, 'VK'), 
               'VTBR':(10000, 'Банк ВТБ'), 
               'MTLR':(1, 'Мечел'),}