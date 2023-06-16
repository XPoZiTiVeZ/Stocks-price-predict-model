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

		# self.model_SBER = model.Model("SBER")
		# self.model_GAZP = model.Model("GAZP")
		# self.model_OGKB = model.Model("OGKB")
		# self.model_FIVE = model.Model("FIVE")
		# self.model_NVTK = model.Model("NVTK")
		# self.model_PIKK = model.Model("PIKK")
		# self.model_ROSN = model.Model("ROSN")
		# self.model_IRAO = model.Model("IRAO")
		# self.model_YNDX = model.Model("YNDX")
		# self.model_VKCO = model.Model("VKCO")
		# self.model_VTBR = model.Model("VTBR")
		# self.model_MTLR = model.Model("MTLR")

		# self.predicted_SBER = -1
		# self.predicted_GAZP = -1
		# self.predicted_OGKB = -1
		# self.predicted_FIVE = -1
		# self.predicted_NVTK = -1
		# self.predicted_PIKK = -1
		# self.predicted_ROSN = -1
		# self.predicted_IRAO = -1
		# self.predicted_YNDX = -1
		# self.predicted_VKCO = -1
		# self.predicted_VTBR = -1
		# self.predicted_MTLR = -1

	
	def parse(self): 
		print("Обращение к парсеру")
		parser1.parse() # Парс актуальных данных

	
	def fit_all_models(self): # Обучение на последних сохранённых данных
		self.fited = {}
		for ticker in ticker_list:
			self.fited[ticker] = self.models[ticker].fit()

		# self.model_SBER.fit()
		# self.model_GAZP.fit()
		# self.model_OGKB.fit()
		# self.model_FIVE.fit()
		# self.model_NVTK.fit()
		# self.model_PIKK.fit()
		# self.model_ROSN.fit()
		# self.model_IRAO.fit()
		# self.model_YNDX.fit()
		# self.model_VKCO.fit()
		# self.model_VTBR.fit()
		# self.model_MTLR.fit()


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

		# self.predicted_GAZP = self.model_GAZP.predict()
		# if not pth.isfile('./predata/GAZP_predata.csv'):
		# 	last_item = pd.read_csv('./data/GAZP_data.csv', parse_dates=['TRADEDATE'])[['TRADEDATE', 'CLOSE']][-1:].to_csv('./predata/GAZP_predata.csv')
		# predataset = pd.read_csv('./predata/GAZP_predata.csv', index_col=0)
		# new_predata = pd.DataFrame({'TRADEDATE': [(datetime.strptime(list(predataset['TRADEDATE'])[-1], '%Y-%m-%d') + pd.Timedelta(days = 1)).strftime('%Y-%m-%d')], 'CLOSE': [self.predicted_GAZP]})
		# new_predataset = pd.concat([predataset, new_predata], ignore_index=True).to_csv('./predata/GAZP_predata.csv')

		# self.predicted_OGKB = self.model_OGKB.predict()
		# if not pth.isfile('./predata/OGKB_predata.csv'):
		# 	last_item = pd.read_csv('./data/OGKB_data.csv', parse_dates=['TRADEDATE'])[['TRADEDATE', 'CLOSE']][-1:].to_csv('./predata/OGKB_predata.csv')
		# predataset = pd.read_csv('./predata/OGKB_predata.csv', index_col=0)
		# new_predata = pd.DataFrame({'TRADEDATE': [(datetime.strptime(list(predataset['TRADEDATE'])[-1], '%Y-%m-%d') + pd.Timedelta(days = 1)).strftime('%Y-%m-%d')], 'CLOSE': [self.predicted_OGKB]})
		# new_predataset = pd.concat([predataset, new_predata], ignore_index=True).to_csv('./predata/OGKB_predata.csv')

		# self.predicted_FIVE = self.model_FIVE.predict()
		# if not pth.isfile('./predata/FIVE_predata.csv'):
		# 	last_item = pd.read_csv('./data/FIVE_data.csv', parse_dates=['TRADEDATE'])[['TRADEDATE', 'CLOSE']][-1:].to_csv('./predata/FIVE_predata.csv')
		# predataset = pd.read_csv('./predata/FIVE_predata.csv', index_col=0)
		# new_predata = pd.DataFrame({'TRADEDATE': [(datetime.strptime(list(predataset['TRADEDATE'])[-1], '%Y-%m-%d') + pd.Timedelta(days = 1)).strftime('%Y-%m-%d')], 'CLOSE': [self.predicted_FIVE]})
		# new_predataset = pd.concat([predataset, new_predata], ignore_index=True).to_csv('./predata/FIVE_predata.csv')

		# self.predicted_NVTK = self.model_NVTK.predict()
		# if not pth.isfile('./predata/NVTK_predata.csv'):
		# 	last_item = pd.read_csv('./data/NVTK_data.csv', parse_dates=['TRADEDATE'])[['TRADEDATE', 'CLOSE']][-1:].to_csv('./predata/NVTK_predata.csv')
		# predataset = pd.read_csv('./predata/NVTK_predata.csv', index_col=0)
		# new_predata = pd.DataFrame({'TRADEDATE': [(datetime.strptime(list(predataset['TRADEDATE'])[-1], '%Y-%m-%d') + pd.Timedelta(days = 1)).strftime('%Y-%m-%d')], 'CLOSE': [self.predicted_NVTK]})
		# new_predataset = pd.concat([predataset, new_predata], ignore_index=True).to_csv('./predata/NVTK_predata.csv')

		# self.predicted_PIKK = self.model_PIKK.predict()
		# if not pth.isfile('./predata/PIKK_predata.csv'):
		# 	last_item = pd.read_csv('./data/PIKK_data.csv', parse_dates=['TRADEDATE'])[['TRADEDATE', 'CLOSE']][-1:].to_csv('./predata/PIKK_predata.csv')
		# predataset = pd.read_csv('./predata/PIKK_predata.csv', index_col=0)
		# new_predata = pd.DataFrame({'TRADEDATE': [(datetime.strptime(list(predataset['TRADEDATE'])[-1], '%Y-%m-%d') + pd.Timedelta(days = 1)).strftime('%Y-%m-%d')], 'CLOSE': [self.predicted_PIKK]})
		# new_predataset = pd.concat([predataset, new_predata], ignore_index=True).to_csv('./predata/PIKK_predata.csv')

		# self.predicted_ROSN = self.model_ROSN.predict()
		# if not pth.isfile('./predata/ROSN_predata.csv'):
		# 	last_item = pd.read_csv('./data/ROSN_data.csv', parse_dates=['TRADEDATE'])[['TRADEDATE', 'CLOSE']][-1:].to_csv('./predata/ROSN_predata.csv')
		# predataset = pd.read_csv('./predata/ROSN_predata.csv', index_col=0)
		# new_predata = pd.DataFrame({'TRADEDATE': [(datetime.strptime(list(predataset['TRADEDATE'])[-1], '%Y-%m-%d') + pd.Timedelta(days = 1)).strftime('%Y-%m-%d')], 'CLOSE': [self.predicted_ROSN]})
		# new_predataset = pd.concat([predataset, new_predata], ignore_index=True).to_csv('./predata/ROSN_predata.csv')

		# self.predicted_IRAO = self.model_IRAO.predict()
		# if not pth.isfile('./predata/IRAO_predata.csv'):
		# 	last_item = pd.read_csv('./data/IRAO_data.csv', parse_dates=['TRADEDATE'])[['TRADEDATE', 'CLOSE']][-1:].to_csv('./predata/IRAO_predata.csv')
		# predataset = pd.read_csv('./predata/IRAO_predata.csv', index_col=0)
		# new_predata = pd.DataFrame({'TRADEDATE': [(datetime.strptime(list(predataset['TRADEDATE'])[-1], '%Y-%m-%d') + pd.Timedelta(days = 1)).strftime('%Y-%m-%d')], 'CLOSE': [self.predicted_IRAO]})
		# new_predataset = pd.concat([predataset, new_predata], ignore_index=True).to_csv('./predata/IRAO_predata.csv')

		# self.predicted_YNDX = self.model_YNDX.predict()
		# if not pth.isfile('./predata/YNDX_predata.csv'):
		# 	last_item = pd.read_csv('./data/YNDX_data.csv', parse_dates=['TRADEDATE'])[['TRADEDATE', 'CLOSE']][-1:].to_csv('./predata/YNDX_predata.csv')
		# predataset = pd.read_csv('./predata/YNDX_predata.csv', index_col=0)
		# new_predata = pd.DataFrame({'TRADEDATE': [(datetime.strptime(list(predataset['TRADEDATE'])[-1], '%Y-%m-%d') + pd.Timedelta(days = 1)).strftime('%Y-%m-%d')], 'CLOSE': [self.predicted_YNDX]})
		# new_predataset = pd.concat([predataset, new_predata], ignore_index=True).to_csv('./predata/YNDX_predata.csv')

		# self.predicted_VKCO = self.model_VKCO.predict()
		# if not pth.isfile('./predata/VKCO_predata.csv'):
		# 	last_item = pd.read_csv('./data/VKCO_data.csv', parse_dates=['TRADEDATE'])[['TRADEDATE', 'CLOSE']][-1:].to_csv('./predata/VKCO_predata.csv')
		# predataset = pd.read_csv('./predata/VKCO_predata.csv', index_col=0)
		# new_predata = pd.DataFrame({'TRADEDATE': [(datetime.strptime(list(predataset['TRADEDATE'])[-1], '%Y-%m-%d') + pd.Timedelta(days = 1)).strftime('%Y-%m-%d')], 'CLOSE': [self.predicted_VKCO]})
		# new_predataset = pd.concat([predataset, new_predata], ignore_index=True).to_csv('./predata/VKCO_predata.csv')

		# self.predicted_VTBR = self.model_VTBR.predict()
		# if not pth.isfile('./predata/VTBR_predata.csv'):
		# 	last_item = pd.read_csv('./data/VTBR_data.csv', parse_dates=['TRADEDATE'])[['TRADEDATE', 'CLOSE']][-1:].to_csv('./predata/VTBR_predata.csv')
		# predataset = pd.read_csv('./predata/VTBR_predata.csv', index_col=0)
		# new_predata = pd.DataFrame({'TRADEDATE': [(datetime.strptime(list(predataset['TRADEDATE'])[-1], '%Y-%m-%d') + pd.Timedelta(days = 1)).strftime('%Y-%m-%d')], 'CLOSE': [self.predicted_VTBR]})
		# new_predataset = pd.concat([predataset, new_predata], ignore_index=True).to_csv('./predata/VTBR_predata.csv')

		# self.predicted_MTLR = self.model_MTLR.predict()
		# if not pth.isfile('./predata/MTLR_predata.csv'):
		# 	last_item = pd.read_csv('./data/MTLR_data.csv', parse_dates=['TRADEDATE'])[['TRADEDATE', 'CLOSE']][-1:].to_csv('./predata/MTLR_predata.csv')
		# predataset = pd.read_csv('./predata/MTLR_predata.csv', index_col=0)
		# new_predata = pd.DataFrame({'TRADEDATE': [(datetime.strptime(list(predataset['TRADEDATE'])[-1], '%Y-%m-%d') + pd.Timedelta(days = 1)).strftime('%Y-%m-%d')], 'CLOSE': [self.predicted_MTLR]})
		# new_predataset = pd.concat([predataset, new_predata], ignore_index=True).to_csv('./predata/MTLR_predata.csv')

	
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