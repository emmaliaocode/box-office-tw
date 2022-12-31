# main.py

from bokeh.io import curdoc
from bokeh.layouts import layout, column, row
from bokeh.models import ColumnDataSource, Div, DataTable, TableColumn, DateFormatter
import pandas as pd

from module import *


# import data
df = pd.read_csv('./data/box_office.csv')


# preprocessing
df.rename(columns={'統計起始日': 'statistic_date', '上映日期': 'release_date', '上映院數': 'theater', '中文片名': 'name',
                     '國別地區': 'country', '累計銷售票數': 'ticket', '累計銷售金額': 'revenue'}, inplace=True)

null_index = df.index[(df['ticket'].isnull()) | (df['revenue'].isnull())]
df = df.drop(null_index)

df['statistic_date'] = preprocessing.datetime_set_format(df['statistic_date'])
df['statistic_year'] = preprocessing.datetime_retrive_year(df['statistic_date'])
df['release_date'] = preprocessing.datetime_set_format(df['release_date'])
df['release_year'] = preprocessing.datetime_retrive_year(df['release_date'])

df['ticket'] = preprocessing.number_set_format(df['ticket'], 'Int64')
df['revenue'] = preprocessing.number_set_format(df['revenue'], 'Float64')

df['revenue_100m'] = preprocessing.number_divide(df['revenue'], 100000000)

df = df.sort_values(['name', 'revenue'], ascending=False).drop_duplicates(
    subset='name', keep='last')
df = df.reset_index(drop=True)

source = ColumnDataSource(data=dict(statistic_date=[], release_date=[], statistic_year=[], release_year=[], theater=[],
                                    name=[], country=[], ticket=[], revenue=[], revenue_100m=[]))
p_source_country = ColumnDataSource(data=dict(country=[], country_count=[]))
p_source_release_year = ColumnDataSource(
    data=dict(release_year=[], release_year_count=[]))


# widgets
statistic_year_select = create_select(df, 'statistic_year')
statistic_year_select.on_change('value', lambda attr, old, new: callback())

country_select = create_select(df, 'country')
country_select.on_change('value', lambda attr, old, new: callback())

revenue_slider = create_slider(df, 'revenue')
revenue_slider.on_change('value', lambda attr, old, new: callback())

ticket_slider = create_slider(df, 'ticket')
ticket_slider.on_change('value', lambda attr, old, new: callback())

theater_slider = create_slider(df, 'theater')
theater_slider.on_change('value', lambda attr, old, new: callback())


def get_select_data():
    revenue_val = revenue_slider.value
    ticket_val = ticket_slider.value
    theater_val = theater_slider.value

    statistic_year_val = statistic_year_select.value
    country_val = country_select.value

    select = df[(df['revenue'] >= revenue_val) &
                (df['ticket'] >= ticket_val) &
                (df['theater'] >= theater_val)]

    if statistic_year_val != '全部':
        select = select[select['statistic_year'].apply(
            lambda x: x == statistic_year_val)]

    if country_val != '全部':
        if country_val == '其他':
            counrty_list = get_column_groups(df, 'country', False)
            select = select[select['country'].apply(
                lambda i: i not in counrty_list)]
        else:
            select = select[select['country'].apply(
                lambda i: i == country_val)]

    select = select.sort_values('revenue', ascending=False)

    return select


def get_plot_data(item):
    new_data = get_select_data()
    p_data = new_data[item]

    if item == 'country':
        col_gp = get_column_groups(new_data, 'country', False)
        gp = [g for g in col_gp if g != '其他']
        summary = pd.Series(
            ['其他' if i not in gp else i for i in p_data]).value_counts()

    if item == 'release_year':
        col_gp = get_column_groups(new_data, 'release_year', False)
        summary = pd.Series(
            [col_gp[-1] if i not in col_gp else i for i in p_data]).value_counts().sort_index(ascending=False)

    p_count = list(summary)
    p_x = list(summary.index)

    p_data = pd.DataFrame({
        'p_x': p_x,
        'p_count': p_count
    })

    return p_data


def callback():
    new_data = get_select_data()
    source.data = dict(
        statistic_date=new_data['statistic_date'],
        release_date=new_data['release_date'],
        statistic_year=new_data['statistic_year'],
        release_year=new_data['release_year'],
        theater=new_data['theater'],
        name=new_data['name'],
        country=new_data['country'],
        ticket=new_data['ticket'],
        revenue=new_data['revenue'],
        revenue_100m=new_data['revenue_100m']
    )

    p_data_country = get_plot_data('country')
    p_source_country.data = dict(
        country=p_data_country['p_x'],
        country_count=p_data_country['p_count']
    )

    p_data_release_year = get_plot_data('release_year')
    p_source_release_year.data = dict(
        release_year=p_data_release_year['p_x'],
        release_year_count=p_data_release_year['p_count']
    )


# plot
p_x_range_statistic_year = get_column_groups(df, 'statistic_year', False)
p_release_year_tooltips = [
    ('name', '@name'),
    ('release_year', '@release_year'),
    ('ticket', '@ticket'),
    ('revenue', '@revenue')
]
p_statistic_year_revenue = create_circle_chart(source=source, x_range=p_x_range_statistic_year,
                                               x_label='statistic_year', y_label='revenue_100m', title='',
                                               tooltips=p_release_year_tooltips, x='statistic_year', y='revenue_100m')

p_x_range_country = get_column_groups(df, 'country', False)
p_tooltips_country = [
    ('country', '@country'),
    ('count', '@country_count')
]
p_country = create_bar_chart(source=p_source_country, x_range=p_x_range_country,
                             x_label='country', y_label='frequency', title='',
                             tooltips=p_tooltips_country, x='country', top='country_count')

p_x_range_release_year = get_column_groups(df, 'release_year', False)
p_release_year_tooltips = [
    ('year', '@release_year'),
    ('count', '@release_year_count')
]
p_release_year = create_bar_chart(source=p_source_release_year, x_range=p_x_range_release_year,
                                  x_label='release_year', y_label='frequency', title='',
                                  tooltips=p_release_year_tooltips, x='release_year', top='release_year_count')


# data table
col = [
    TableColumn(field='statistic_year', title='statistic_year'),
    TableColumn(field='release_year', title='release_year'),
    TableColumn(field='theater', title='theater'),
    TableColumn(field='name', title='name'),
    TableColumn(field='country', title='country'),
    TableColumn(field='ticket', title='ticket'),
    TableColumn(field='revenue', title='revenue')
    # TableColumn(field='date', title='date',
    #             formatter=DateFormatter()),
    # TableColumn(field='release', title='release',
    #             formatter=DateFormatter()),
]
datatable = DataTable(width=1200, height=380, source=source,
                      columns=col, margin=(15, 0, 0, 15))


# html
index = Div(text=open('./app/index.html').read(), sizing_mode='stretch_both')
widgets = [statistic_year_select, country_select,
           revenue_slider, ticket_slider, theater_slider]
layout = layout(
    [index],
    [widgets],
    [p_statistic_year_revenue, p_country, p_release_year],
    [datatable]
)

callback()

curdoc().add_root(layout)
curdoc().title = 'TW Box office'
