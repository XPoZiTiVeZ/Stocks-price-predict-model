from flask import Flask, render_template
from posrednik import Posrednik
import pandas as pd
import plotly.express as px
import visual
from threading import Thread
from model import get_ticker_list, get_act_name

app = Flask('', static_url_path='/static')


@app.route('/')
def home():
    return render_template('home.html', tickers=get_ticker_list())

@app.route('/plots/<stock>')
def plots(stock):
    stock = stock.upper()
    if stock in get_ticker_list():
        graphJSON = visual.getplot_image(f"{stock}", rf'./data/{stock}_data.csv', rf'./predict_data/{stock}_predict_data.csv')
    else:
        return "Не найдено такой акции"
    return render_template('plot.html', graphJSON=graphJSON, stock=get_act_name(stock), tickers=get_ticker_list())

def run():
    print('Сайт запущен!')
    app.run(host="127.0.0.1", port=80)

def start():
    Thread(target=run).start()
    

if __name__ == "__main__":
    run()