from flask import Flask, render_template
from visual import getplot
from threading import Thread
from config import ticker_info, data_path, predict_data_path

app = Flask('', static_url_path='/static')


@app.route('/')
def home():
    return render_template('home.html', tickers=ticker_info.keys())


@app.route('/plots/<stock>')
def plots(stock):
    stock = stock.upper()
    if stock in ticker_info.keys():
        return render_template('plot.html', graphJSON=getplot(stock, data_path(stock), predict_data_path(stock)), stock=ticker_info.get(stock)[1], tickers=ticker_info.keys())
    else:
        return render_template('404plot.html', found=False)


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


@app.errorhandler(500)
def page_not_found(e):
    return render_template('500.html'), 500


def run():
    print('Сайт запущен!')
    app.run(host="127.0.0.1", port=80)


def start():
    Thread(target=run).start()
    

if __name__ == "__main__":
    run()