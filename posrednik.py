#posrednik by @igorar666

# Импорт всех модулей программы
import parser1
import model
import os.path as pth
import pandas as pd
from threading import Timer
from datetime import datetime
from visual import getplot_image
from config import ticker_info, data_path, predict_data_path, plots_path, mq_plots_path

# Класс для того чтоб было красивее и чтука проще
class Posrednik():
	def __init__(self): # helper = Posrednik()
		print("Инициализация посредника")

		self.ticker_list = ticker_info.keys()
  
		self.models = {}
		for ticker in self.ticker_list:
			self.models[ticker] = model.Model(ticker)

	
	def parse(self): 
		print("Обращение к парсеру")
		parser1.parse() # Парс актуальных данных
	
	
	def fit_all_models(self): # Обучение на последних сохранённых данных
		self.fited = {}
		for ticker in self.ticker_list:
			self.fited[ticker] = self.models[ticker].fit()


	def predict_all_models(self): # Предсказание на сохранённых моделях
		print("Предсказывание моделей")
		self.predicted = {}
		for ticker in self.ticker_list:
			self.predicted[ticker] = self.models[ticker].predict()
			if not pth.isfile(predict_data_path(ticker)):
				pd.read_csv(data_path(ticker), parse_dates=['TRADEDATE'])[['TRADEDATE', 'CLOSE']][-1:].to_csv(predict_data_path(ticker))
			predict_dataset = pd.read_csv(predict_data_path(ticker), index_col=0)
			if list(predict_dataset['TRADEDATE'])[-1] == datetime.today().strftime('%Y-%m-%d'):
				predict_dataset = predict_dataset[predict_dataset['TRADEDATE'] != datetime.today().strftime('%Y-%m-%d')]
			new_predict_data = pd.DataFrame({'TRADEDATE': [(datetime.strptime(list(predict_dataset['TRADEDATE'])[-1], '%Y-%m-%d') + pd.Timedelta(days = 1)).strftime('%Y-%m-%d')], 'CLOSE': [self.predicted[ticker]]})
			pd.concat([predict_dataset, new_predict_data], ignore_index=True).to_csv(predict_data_path(ticker))


	def get_all_plots(self): # Создание графиков
		for ticker in self.ticker_list:
			getplot_image(ticker, data_path(ticker), predict_data_path(ticker))

	
	def main(self): # Поочерёдный запуск всех функций
		print("Работа посредника")
		self.parse()
		self.fit_all_models()
		self.predict_all_models()
		self.get_all_plots()
		self.que = Timer(86400, self.main) # Через сутки всё повторится
		print('Программа запущена и готова к работе')
	
 
if __name__ == '__main__':
	Posrednik().main()