from flask import Flask, render_template
from posrednik import Posrednik
import pandas as pd
import plotly.express as px
import visual
from threading import Thread
from config import ticker_list

app = Flask('', static_url_path='/static')


translate = {'SBER':'сбербанк', 'GAZP':'газпром', 'OGKB':'ОГК-2', 'FIVE':'X5 Group', 'NVTK':'новатэк', 'PIKK':'ГРУППА КОМПАНИЙ ПИК',
               'ROSN':'роснефть', 'IRAO':'интер РАО', 'YNDX':'яндекс', 'VKCO':'VK', 'VTBR':'банк ВТБ', 'MTLR':'meltron AB'}

@app.route('/')
def home():
    return render_template('home.html', tickers = ticker_list)

@app.route('/plots/<stock>')
def plots(stock):
    stock = stock.upper()
    if stock in ticker_list:
        graphJSON = visual.getplot(f"{stock}", rf'./data/{stock}_data.csv', rf'./predata/{stock}_predata.csv')
    else:
        return "Не найдено такой акции"
    return render_template('plot.html', graphJSON=graphJSON, stock=translate.get(stock), tickers = ticker_list)

def run():
    print('Сайт запущен!')
    app.run(host="127.0.0.1", port=8080)

def start():
    Thread(target=run).start()

if __name__ == "__main__":
    run()