# main.py

# todo:
#   - add annual/weekly (RadioButtonGroup)
#   - add filter

from bokeh.io import curdoc
from bokeh.layouts import column, row
from bokeh.models import ColumnDataSource, Div, Slider, DataTable, TableColumn, DateFormatter
from bokeh.plotting import figure
import pandas as pd

# import dataset
df = pd.read_csv('./data/box_office.csv')

# dataset preprocessing
df.rename(columns={'統計起始日': 'date', '上映日期': 'release', '上映院數': 'theaters', '中文片名': 'name',
          '國別地區': 'country', '累計銷售票數': 'tickets', '累計銷售金額': 'revenue'}, inplace=True)
df['date'] = pd.to_datetime(df['date'])
df['release'] = pd.to_datetime(df['release'])
df['tickets'] = df['tickets'].str.replace(',', '')
df['tickets'] = pd.to_numeric(df['tickets']).astype('Int64')
df['revenue'] = df['revenue'].str.replace(',', '')
df['revenue'] = pd.to_numeric(df['revenue']).astype('Float64')
df['revenue_10k'] = df['revenue'].div(10000)
null_index = df.index[(df['tickets'].isnull()) | (df['revenue_10k'].isnull())]
df = df.drop(null_index)

source = ColumnDataSource(data=dict(date=[], release=[], theaters=[], name=[
], country=[], tickets=[], revenue=[], revenue_10k=[]))

# plot
tooltips = [
    ('Movie', '@name'),
    ('Tickets', '@tickets'),
    ('NT$', '@revenue')
]
plot = figure(width=850, height=280, tooltips=tooltips,
              toolbar_location=None, sizing_mode='scale_both', title='')
plot.circle(x='tickets', y='revenue', source=source, size=5)

# data table
columns = [
    TableColumn(field='date', title='Statistic date',
                formatter=DateFormatter()),
    TableColumn(field='release', title='Released date',
                formatter=DateFormatter()),
    TableColumn(field='theaters', title='Theaters'),
    TableColumn(field='name', title='Movie'),
    TableColumn(field='country', title='Country'),
    TableColumn(field='tickets', title='Tickets'),
    TableColumn(field='revenue', title='NT$')
]
datatable = DataTable(width=850, height=280, source=source,
                      columns=columns, sortable=True)

# widget
# todo: add filters
ticket_slider = Slider(start=0, end=max(
    df['tickets']), value=0, step=100000, title='Tickets sold greater than')
ticket_slider.on_change('value', lambda attr, old, new: callback())


def selected():
    # todo: add filters
    ticket_val = ticket_slider.value
    selected = df[df['tickets'] >= ticket_val]
    return selected


def callback():
    # todo: add filters
    df = selected()
    plot.title.text = '%d movies selected' % len(df)
    source.data = dict(
        date=df['date'],
        release=df['release'],
        theaters=df['theaters'],
        name=df['name'],
        country=df['country'],
        tickets=df['tickets'],
        revenue=df['revenue'],
        revenue_10k=df['revenue_10k']
    )


# html
index = Div(text=open('./app/index.html').read(), sizing_mode='stretch_width')
footer = Div(text=open('./app/footer.html').read(),
             sizing_mode='stretch_width')
# todo: add filters
filters = column(ticket_slider)
results = column(plot, datatable)

layout = column(row(index), row(filters, results),
                row(footer), sizing_mode='scale_both')
callback()

curdoc().add_root(layout)
curdoc().title = 'Box office TW'
