# main.py

import pandas as pd
from os.path import dirname, join

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Div, Slider
from bokeh.plotting import figure, show

# import dataset
df = pd.read_csv('./data/box_office_dataset.csv')

# dataset preprocessing
df['統計起始日'] = pd.to_datetime(df['統計起始日'])
df['上映日期'] = pd.to_datetime(df['上映日期'])
df['累計銷售票數'] = pd.to_numeric(df['累計銷售票數'].str.replace(',', '')).astype('Int64')
df['累計銷售金額'] = pd.to_numeric(df['累計銷售金額'].str.replace(',', '')).astype('Float64')
df['累計銷售金額_萬'] = df['累計銷售金額'].div(10000)
null_index = df.index[(df['累計銷售票數'].isnull()) | (df['累計銷售金額'].isnull())]
df = df.drop(null_index)

source = ColumnDataSource(data = dict(上映日期 = [], 上映院數 = [], 中文片名 = [], 國別地區 = [], 累計銷售票數 = [], 累計銷售金額 = [], 累計銷售金額_萬 = []))

# functions
def selected():
    # todo: add filters
    ticket_val = ticket_slider.value
    selected = df[df['累計銷售票數'] >= ticket_val]
    return selected

def callback():
    # todo: add filters
    df = selected()
    p.title.text = '%d movies selected' % len(df)
    source.data = dict(
        累計銷售票數 = df['累計銷售票數'],
        累計銷售金額 = df['累計銷售金額']
    )

# widget
# todo: add filters
ticket_slider = Slider(start = 0, end = max(df['累計銷售票數']), value = 0, step = 100000, title = '累計銷售票數大於')
ticket_slider.on_change('value', lambda attr, old, new: callback())

# plot
p = figure(width = 600, height = 350, toolbar_location = None, sizing_mode = 'scale_both', title = '')
p.circle(x = '累計銷售票數', y = '累計銷售金額', source = source)

# html
index = Div(text = open('./app/index.html').read(), sizing_mode = 'stretch_width')
footer = Div(text = open('./app/footer.html').read(), sizing_mode = 'stretch_width')
# todo: add filters
filters = column(ticket_slider, width = 320)

l = column(row(index), row(filters, p), row(footer), sizing_mode = "scale_both")
callback()

curdoc().add_root(l)
curdoc().title = "Box office TW"
