#model by @igorar666 and @Belkinark

import tensorflow as tf
from keras.callbacks import EarlyStopping
import numpy as np
import pandas as pd
import math
import matplotlib.pyplot as plt
from datetime import datetime


def get_ticker_list():
	ticker_list = ['SBER', 'GAZP', 'OGKB', 'FIVE', 'NVTK','PIKK',
				'ROSN', 'IRAO', 'YNDX', 'VKCO', 'VTBR', 'MTLR']
	return ticker_list

def get_act_name(ticker):
    name = {'SBER':'Сбербанк', 'GAZP':'Газпром', 'OGKB':'ОГК-2', 'FIVE':'X5 Group', 'NVTK':'Новатэк', 'PIKK':'ГРУППА КОМПАНИЙ ПИК',
               'ROSN':'Роснефть', 'IRAO':'Интер РАО', 'YNDX':'Яндекс', 'VKCO':'VK', 'VTBR':'Банк ВТБ', 'MTLR':'Мечел'}
    return name.get(ticker)


def get_lot_info(ticker):
	lot = {'SBER': 10, 'GAZP': 10, 'OGKB': 1000, 'FIVE': 1, 'NVTK': 1,
        'PIKK': 1, 'ROSN': 1, 'IRAO': 100, 'YNDX': 1, 'VKCO': 1, 'MTLR': 1, 
        'VTBR': 10000}
	return lot.get(ticker)


def get_round_num(ticker):
	if get_lot_info(ticker) < 100:
		round_num = 2
	elif get_lot_info(ticker) < 10000:
		round_num = 4
	else:
		round_num = 6
	return round_num


class Model():
	def __init__(self, stock):
		print("Инициализация нейронки")
		self.stock = stock
		
		# Stock это код акции которая будет предсказываться

	def normalise_window(self, window_data, single_window=False):
		normalised_data = []
		window_data = [window_data] if single_window else window_data

		for window in window_data:
			normalised_window = []
			for col_i in range(window.shape[1]):
				normalised_col = [((float(p) / float(window[0, col_i])) - 1) for p in window[:, col_i]]
				normalised_window.append(normalised_col)
			normalised_window = np.array(normalised_window).T
			normalised_data.append(normalised_window)

		return np.array(normalised_data)
	

	def _next_window(self, i, seq_len, normalise):
		window = self.data_train[i:i+seq_len]
		window = self.normalise_window(window, single_window=True)[0] if normalise else window

		x = window[:-1]
		y = window[-1, [0]]

		return x, y
	
	def get_train_data(self, seq_len, normalise):
		self.data_x = []
		self.data_y = []

		for i in range(self.len_train - seq_len + 1):
			x, y = self._next_window(i, seq_len, normalise)
			self.data_x.append(x)
			self.data_y.append(y)
		
		return np.array(self.data_x), np.array(self.data_y)
	
	def get_test_data(self, seq_len, normalise):
		data_window = []
		for i in range(self.len_test - seq_len):
			data_window.append(self.data_test[i:i+seq_len])
		
		data_window = np.array(data_window).astype(float)
		data_window = self.normalise_window(data_window, single_window=False) if normalise else data_window

		x = data_window[:, :-1]
		y = data_window[:, -1, [0]]

		return x, y

	def get_last_data(self, seq_len, normalise):
		last_data = self.data_test[seq_len:]
		data_window = np.array(last_data).astype(float)
		data_window = self.normalise_window(data_window, single_window=True) if normalise else data_window
		return data_window
	
	def de_normalise_predicted(self, price_1st, _data):
		return (_data + 1) * price_1st

	def fit(self):
		print(f"Обучение нейронки {self.stock}")
		self.df = pd.read_csv(f"./data/{self.stock}_data.csv", sep=",")

		split = 0.85
		i_split = int(len(self.df) * split)
		cols = ["CLOSE", "VOLUME"]

		self.data_train = self.df.get(cols).values[:i_split] # type: ignore
		self.data_test = self.df.get(cols).values[i_split:] # type: ignore

		self.len_train = len(self.data_train)
		self.len_test = len(self.data_test)

		sequence_length = 5
		input_dim = 2
		batch_size = 16
		

		model = tf.keras.Sequential([
				tf.keras.layers.LSTM(100, input_shape=(sequence_length-1, input_dim), return_sequences=True),
				tf.keras.layers.Dropout(.2),
				tf.keras.layers.LSTM(100, return_sequences=True),
				tf.keras.layers.LSTM(100, return_sequences=False),
				tf.keras.layers.Dropout(.2),
				tf.keras.layers.Dense(1, activation="linear"),
			])

		model.compile(optimizer="adam",
				loss="mse",
				metrics=["accuracy"])
			
		x, y = self.get_train_data(
				seq_len=sequence_length,
				normalise=True
			)
			
		callbacks = [EarlyStopping(monitor="accuracy", patience=2)]

		while True:
			epochs = 2
			model.fit(x, y, epochs=epochs, batch_size=batch_size, callbacks=callbacks)


			x_test, y_test = self.get_test_data(sequence_length, True)

			loss = model.evaluate(x_test, y_test, verbose=2)[0] # type: ignore
			print(f"{self.stock} Loss = {loss}")
			if loss < 0.01:
				break
			print("Переобучение...")


		last_data_2_predict_prices = self.get_last_data(-(sequence_length-1), False)
		self.last_data_2_predict_prices_1st_price = last_data_2_predict_prices[0][0]
		self.last_data_2_predict = self.get_last_data(-(sequence_length-1), True)

		self.model = model
		# Тут будет открытие файла и обучение
		

	def predict(self):
		predictions2 = self.model.predict(self.last_data_2_predict)
		predicted_price = self.de_normalise_predicted(self.last_data_2_predict_prices_1st_price, predictions2[0][0])
		print(f"{self.stock} prediction is {round(predicted_price, get_round_num(self.stock))}")
		return round(predicted_price, get_round_num(self.stock))


if __name__ == "__main__":
	ticker = "IRAO"
	model = Model(ticker)
	print(model)
	model.fit()
	print(round(model.predict(), get_round_num(ticker)))

