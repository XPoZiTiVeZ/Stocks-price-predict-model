#posrednik by @igorar666

# Импорт всех модулей программы
import parser1
import model
import threading
import visual


# Класс для того чтоб было красивее и чтука проще
class Posrednik():
	def __init__(self): # helper = Posrednik()
		print("Инициализация посредника")

		ticker_list = ['SBER', 'GAZP', 'OGKB', 'FIVE', 'NVTK',
                 'PIKK', 'ROSN', 'IRAO', 'YNDX', 'VKCO', 'VTBR', 
                 'MTLR']
		
		self.model_SBER = model.Model("SBER")
		self.model_GAZP = model.Model("GAZP")
		self.model_OGKB = model.Model("OGKB")
		self.model_FIVE = model.Model("FIVE")
		self.model_NVTK = model.Model("NVTK")
		self.model_PIKK = model.Model("PIKK")
		self.model_ROSN = model.Model("ROSN")
		self.model_IRAO = model.Model("IRAO")
		self.model_YNDX = model.Model("YNDX")
		self.model_VKCO = model.Model("VKCO")
		self.model_VTBR = model.Model("VTBR")
		self.model_MTLR = model.Model("MTLR")


		
		self.predicted_SBER = -1
		self.predicted_GAZP = -1
		self.predicted_OGKB = -1
		self.predicted_FIVE = -1
		self.predicted_NVTK = -1
		self.predicted_PIKK = -1
		self.predicted_ROSN = -1
		self.predicted_IRAO = -1
		self.predicted_YNDX = -1
		self.predicted_VKCO = -1
		self.predicted_VTBR = -1
		self.predicted_MTLR = -1

	
	def parse(self): 
		print("Обращение к парсеру")
		parser1.parse() # Парс актуальных данных
	
	def fit_all_models(self): # Обучение на последних сохранённых данных
		self.model_SBER.fit()
		self.model_GAZP.fit()
		self.model_OGKB.fit()
		self.model_FIVE.fit()
		self.model_NVTK.fit()
		self.model_PIKK.fit()
		self.model_ROSN.fit()
		self.model_IRAO.fit()
		self.model_YNDX.fit()
		self.model_VKCO.fit()
		self.model_VTBR.fit()
		self.model_MTLR.fit()


	def predict_all_models(self): # Предсказание на сохранённых моделях
		print("Предсказывание моделей")
		self.predicted_SBER = self.model_SBER.predict()
		self.predicted_GAZP = self.model_GAZP.predict()
		self.predicted_OGKB = self.model_OGKB.predict()
		self.predicted_FIVE = self.model_FIVE.predict()
		self.predicted_NVTK = self.model_NVTK.predict()
		self.predicted_PIKK = self.model_PIKK.predict()
		self.predicted_ROSN = self.model_ROSN.predict()
		self.predicted_IRAO = self.model_IRAO.predict()
		self.predicted_YNDX = self.model_YNDX.predict()
		self.predicted_VKCO = self.model_VKCO.predict()
		self.predicted_VTBR = self.model_VTBR.predict()
		self.predicted_MTLR = self.model_MTLR.predict()

	
	def get_all_plots(self): # Создание графиков
		visual.getplot("SBER", 'data/SBER_data.csv', self.predicted_SBER)
		visual.getplot("GAZP", 'data/GAZP_data.csv', self.predicted_GAZP)
		visual.getplot("OGKB", r'data/OGKB_data.csv', self.predicted_OGKB)
		visual.getplot("FIVE", r'data/FIVE_data.csv', self.predicted_FIVE)
		visual.getplot("NVTK", r'data/NVTK_data.csv', self.predicted_NVTK)
		visual.getplot("PIKK", r'data/PIKK_data.csv', self.predicted_PIKK)
		visual.getplot("ROSN", r'data/ROSN_data.csv', self.predicted_ROSN)
		visual.getplot("IRAO", r'data/IRAO_data.csv', self.predicted_IRAO)
		visual.getplot("YNDX", r'data/YNDX_data.csv', self.predicted_YNDX)
		visual.getplot("VKCO", r'data/VKCO_data.csv', self.predicted_VKCO)
		visual.getplot("VTBR", r'data/VTBR_data.csv', self.predicted_VTBR)
		visual.getplot("MTLR", r'data/MTLR_data.csv', self.predicted_MTLR)
	
	
	def main(self): # Поочерёдный запуск всех функций
		print("Работа посредника")
		self.parse()
		self.fit_all_models()
		self.predict_all_models()
		self.get_all_plots()
		self.qwe = threading.Timer(86400, self.main) # Через сутки всё повторится
	
