import plotly.graph_objects as go
import pandas as pd
import plotly
import plotly.io as pio
import json
from threading import Thread
from datetime import datetime
from math import ceil, floor
from model import get_round_num



# Функция сохранения графика
def getplot(name: str, file: str, predict_file: str, max_quality=False) -> None:
    
    dataset = pd.read_csv(file, index_col='TRADEDATE', parse_dates=['TRADEDATE'])[-30:].dropna()
    try:
        predict_dataset = pd.read_csv(predict_file, index_col='TRADEDATE', parse_dates=['TRADEDATE'])[-30:]
    except:
        predict_dataset = pd.read_csv(predict_file, index_col='TRADEDATE', parse_dates=['TRADEDATE'])

    maxn = max(dataset['CLOSE'])
    minn = min(dataset['CLOSE'])
    mean = round((minn + maxn)/2, get_round_num(name))
    now = dataset['CLOSE'][-1]

    # графики:
    layout = go.Layout(title=dict(text = f'{name} stock price',
                        font = dict(color = 'black')),
                        plot_bgcolor='black')

    fig = go.Figure(layout = layout)

    fig.add_hline(y = maxn, line_color = 'green',
                annotation=dict(
                    text=f'Максимальная цена {maxn}',
                    align = 'right',
                    font = dict(color = 'green')
                ))

    fig.add_hline(y = mean, line_color='lightgrey',
                annotation=dict(
                    text=f'Средняя цена {mean}',
                    align='right',
                    font = dict(color = 'lightgrey')))

    fig.add_hline(y = minn, line_color='red',
                annotation=dict(
                    text=f'Минимальная цена {minn}',
                    align='right',
                    font = dict(color = 'red')))

    fig.add_hline(y = now, line_color='lightgreen',
                line_dash = 'dash',
                annotation=dict(
                    text=f'Цена сейчас {now}',
                    align='right',
                    font = dict(color = 'lightgreen')))

    fig.add_hline(y = predict_dataset['CLOSE'][-1], line_color='orange',
                line_dash = 'dash',
                annotation=dict(
                    text=f'Предсказанная цена {predict_dataset["CLOSE"][-1]}',
                    align='right',
                    font = dict(color = 'orange')))

    fig.add_trace(go.Scatter(x = dataset.index,
                            y = dataset['CLOSE'],
                            mode = 'lines',
                            name = 'Реальная цена'))
                    
    fig.add_trace(go.Scatter(x = predict_dataset.index,
                            y = predict_dataset['CLOSE'],
                            mode = 'lines',
                            name = 'Предсказанная цена'))

    # настройки:
    fig.update_layout(hovermode="x",
                    legend_orientation="v",
                    legend=dict(x=.5, xanchor="center"),
                    xaxis_tickformat = '%d %B<br>%Y',
                    margin=dict(l=10, r=10, t=30, b=10), width=900, height=1200)

    fig.update_traces(hoverinfo="all", hovertemplate='Цена: %{y}')
    fig.update_xaxes(griddash="dash")
    fig.update_yaxes(tick0 = 0, dtick = round((maxn - minn) / 7, get_round_num(name)))
    # fig.show()
    # экспорт
    if max_quality:
        Thread(target=pio.write_image(fig, f'./mq_plots/MQ_{name}_plot.png', format='png', scale=9, width=1440, height=1920))
    else:
        Thread(target=pio.write_image(fig, f'./plots/{name}_plot.png', format='png', scale=2, width=1440, height=1920))




def getplot_image(name: str, file: str, predict_file: str) -> json:

    dataset = pd.read_csv(file, index_col='TRADEDATE', parse_dates=['TRADEDATE']).dropna()
    try:
        predict_dataset = pd.read_csv(predict_file, index_col='TRADEDATE', parse_dates=['TRADEDATE'])
    except:
        predict_dataset = pd.read_csv(predict_file, index_col='TRADEDATE', parse_dates=['TRADEDATE'])

    # maxnr = ceil(max(dataset[-(30-len(predict_dataset.index)):]['CLOSE']) / 50) * 50
    # minnr = floor(min(dataset[-(30-len(predict_dataset.index)):]['CLOSE']) / 50) * 50
    maxnr = max(dataset[-(30-len(predict_dataset.index)):]['CLOSE']) + 5
    minnr = min(dataset[-(30-len(predict_dataset.index)):]['CLOSE']) - 5
    maxn = max(dataset['CLOSE'])
    minn = min(dataset['CLOSE'])
    mean = round((minn + maxn)/2, 2)
    now = dataset['CLOSE'][-1]

    # графики:
    layout = go.Layout(plot_bgcolor='black')

    fig = go.Figure(layout = layout)

    fig.add_hline(y = maxn, line_color = 'green',
                annotation=dict(
                    text=f'Максимальная цена {maxn}',
                    align = 'right',
                    font = dict(color = 'green')
                ))

    fig.add_hline(y = mean, line_color='lightgrey',
                annotation=dict(
                    text=f'Средняя цена {mean}',
                    align='right',
                    font = dict(color = 'lightgrey')))

    fig.add_hline(y = minn, line_color='red',
                annotation=dict(
                    text=f'Минимальная цена {minn}',
                    align='right',
                    font = dict(color = 'red')))

    fig.add_hline(y = now, line_color='lightgreen',
                line_dash = 'dash',
                annotation=dict(
                    text=f'Цена сейчас {now}',
                    align='right',
                    xanchor='right',
                    yanchor='middle',
                    font = dict(color = 'lightgreen')))

    fig.add_hline(y = predict_dataset['CLOSE'][-1], line_color='orange',
                line_dash = 'dash',
                annotation=dict(
                    text=f'Предсказанная цена {predict_dataset["CLOSE"][-1]}',
                    align='right',
                    xanchor='right',
                    yanchor='middle',
                    font = dict(color = 'orange')))

    fig.add_trace(go.Scatter(x = dataset.index,
                            y = dataset['CLOSE'],
                            mode = 'lines',
                            name = 'Реальная цена'))
    
    fig.add_trace(go.Scatter(x = predict_dataset.index,
                            y = predict_dataset['CLOSE'],
                            mode = 'lines',
                            name = 'Предсказанная цена'))

    # настройки:
    fig.update_layout(hovermode="x",
            showlegend = False,
            xaxis_range = [list(dataset.index)[-(30-len(predict_dataset.index))], (list(predict_dataset.index)[-1] + pd.Timedelta(days = 1)).strftime('%Y-%m-%d')],
            yaxis_range = [minnr, maxnr],
            xaxis_tickformat = '%d %B<br>%Y',
            margin=dict(l=10, r=35, t=30, b=10), height=800)

    fig.update_traces(hoverinfo="all", hovertemplate='Цена: %{y}')
    fig.update_xaxes(griddash="dash")
    fig.update_yaxes(tick0 = 0, dtick = round((maxn - minn) / 7, get_round_num(name)))
    # fig.show()
    return json.dumps(fig, cls=plotly.utils.PlotlyJSONEncoder)

if __name__ == "__main__":
    getplot(f"SBER", rf'./data/SBER_data.csv', rf'./predict_data/SBER_predict_data.csv')