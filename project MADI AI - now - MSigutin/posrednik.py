#posrednik by @igorar666

# Импорт всех модулей программы
import parser1
import model
import threading
import visual
import os.path as pth
import pandas as pd
from datetime import datetime




# Класс для того чтоб было красивее и чтука проще
class Posrednik():
	def __init__(self): # helper = Posrednik()
		print("Инициализация посредника")

		self.ticker_list = model.get_ticker_list()
  
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
			if not pth.isfile(f'./predict_data/{ticker}_predict_data.csv'):
				last_item = pd.read_csv(f'./data/{ticker}_data.csv', parse_dates=['TRADEDATE'])[['TRADEDATE', 'CLOSE']][-1:].to_csv(f'./predict_data/{ticker}_predict_data.csv')
			predict_dataset = pd.read_csv(f'./predict_data/{ticker}_predict_data.csv', index_col=0)
			new_predict_data = pd.DataFrame({'TRADEDATE': [(datetime.strptime(list(predict_dataset['TRADEDATE'])[-1], '%Y-%m-%d') + pd.Timedelta(days = 1)).strftime('%Y-%m-%d')], 'CLOSE': [self.get_stock_predicts(ticker)]})
			new_predict_dataset = pd.concat([predict_dataset, new_predict_data], ignore_index=True).to_csv(f'./predict_data/{ticker}_predict_data.csv')
		

	def get_stock_predicts(self, ticker):
		return self.predicted.get(ticker)

			
 
	def get_all_plots(self): # Создание графиков
		for ticker in self.ticker_list:
			visual.getplot(ticker, rf'./data/{ticker}_data.csv', rf'./predict_data/{ticker}_predict_data.csv')


	
	def main(self): # Поочерёдный запуск всех функций
		print("Работа посредника")
		self.parse()
		self.fit_all_models()
		self.predict_all_models()
		self.get_all_plots()
		self.qwe = threading.Timer(86400, self.main) # Через сутки всё повторится
	
 
if __name__ == '__main__':
	Posrednik().predict_all_models()