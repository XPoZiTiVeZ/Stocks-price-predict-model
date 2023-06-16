#posrednik by @igorar666

# Импорт всех модулей программы
import parser1
import model
import threading
import visual
import os.path as pth
import pandas as pd
from datetime import datetime
from config import ticker_list


# Класс для того чтоб было красивее и чтука проще
class Posrednik():
	def __init__(self): # helper = Posrednik()
		print("Инициализация посредника")
		
		self.models = {}
		for ticker in ticker_list:
			self.models[ticker] = model.Model(ticker)

	
	def parse(self): 
		print("Обращение к парсеру")
		parser1.parse() # Парс актуальных данных

	
	def fit_all_models(self): # Обучение на последних сохранённых данных
		self.fited = {}
		for ticker in ticker_list:
			self.fited[ticker] = self.models[ticker].fit()


	def predict_all_models(self): # Предсказание на сохранённых моделях
		print("Предсказывание моделей")

		self.predicted = {}
		for ticker in ticker_list:
			self.predicted[ticker] = self.models[ticker].predict()
			if not pth.isfile(f'./predata/{ticker}_predata.csv'):
				last_item = pd.read_csv(f'./data/{ticker}_data.csv', parse_dates=['TRADEDATE'])[['TRADEDATE', 'CLOSE']][-1:].to_csv(f'./predata/{ticker}_predata.csv')
			predataset = pd.read_csv(f'./predata/{ticker}_predata.csv', index_col=0)
			new_predata = pd.DataFrame({'TRADEDATE': [(datetime.strptime(list(predataset['TRADEDATE'])[-1], '%Y-%m-%d') + pd.Timedelta(days = 1)).strftime('%Y-%m-%d')], 'CLOSE': [self.predicted[ticker]]})
			new_predataset = pd.concat([predataset, new_predata], ignore_index=True).to_csv(f'./predata/{ticker}_predata.csv')

	
	def get_all_plots(self): # Создание графиков
		for ticker in ticker_list:
			visual.getplot_image(f"{ticker}", rf'./data/{ticker}_data.csv', rf'./predata/{ticker}_predata.csv')
			visual.getplot_image(f"{ticker}", rf'./data/{ticker}_data.csv', rf'./predata/{ticker}_predata.csv', max_quality=True)
	
	
	def main(self): # Поочерёдный запуск всех функций
		print("Работа посредника")
		self.parse()
		self.fit_all_models()
		self.predict_all_models()
		self.get_all_plots()
		self.qwe = threading.Timer(86400, self.main) # Через сутки всё повторится
	
if __name__ == '__main__':
	Posrednik().predict_all_models()