# module.py

from bokeh.models import Select, Slider, PrintfTickFormatter
from bokeh.plotting import figure
import datetime
from math import pi
import pandas as pd

# general
def get_time():
    return datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')


# download dataset
class response_results:
    def shape_data_list(keep_id_list, responses):
        urls = []
        data_list = []
        for jj in keep_id_list:
            filename = responses[jj]['resourceDescription']
            start_date = filename.split('至')[0]
            start_date = start_date.replace('年', '/')
            start_date = start_date.replace('月', '/')
            start_date = start_date.replace('日', '')
            url = responses[jj]['resourceDownloadUrl']
            urls.append(url)
            table = pd.read_csv(url)
            table['統計起始日'] = start_date
            data_list.append(table)
        return data_list

    def data_list_to_data_frame(data_list):
        data = pd.concat(data_list, axis=0)
        new_colname = ['統計起始日', '上映日期', '中文片名',
                       '國別地區', '上映院數', '累計銷售票數', '累計銷售金額']
        return data[new_colname]

    def fix_data_bug(data):
        data = data.replace({'上映日期': '2019/0807'}, '2019/08/07')
        return data


# preprocessing
class preprocessing:
    def datetime_set_format(column):
        return pd.to_datetime(column)

    def datetime_retrive_year(column):
        return column.apply(lambda d: str(d.year))

    def number_set_format(column, num_type):
        tmp = column.apply(lambda d: str(d).replace(',', ''))
        return pd.to_numeric(tmp).astype(num_type)

    def number_divide(column, num_div):
        return column.div(num_div)


# bokeh widgets
def get_column_groups(df, item, append):
    count = df[item].value_counts()
    gp = list(count.index)

    if item == 'statistic_year':
        options = sorted(gp, reverse=True)

    if item == 'country':
        options = gp[:9]
        options.append('其他')

    if item == 'release_year':
        options = sorted(gp[:9], reverse=True)
        options.append(options[-1] + ' 年前')

    if append:
        options.insert(0, '全部')

    return list(options)


def create_select(df, item):
    options = get_column_groups(df, item, True)

    if item == 'statistic_year':
        title = '年份'
        value = '全部'

    if item == 'country':
        title = '國別地區'
        value = '全部'

    return Select(title=title, options=options, value=value, margin=(5, 5, 5, 15))


def create_slider(df, item):
    maximum = max(df[item])
    start = 0
    value = start

    if item == 'revenue':
        title = '累積票房大於'
        step = 100000

    if item == 'ticket':
        title = '累積售票大於'
        step = 100000

    if item == 'theater':
        title = '上映院數大於'
        step = 10

    return Slider(title=title, start=start, end=maximum, step=step, value=value, margin=(5, 5, 5, 15))


# bokeh plots
def create_bar_chart(source, x_range, x_label, y_label, title, tooltips, x, top):
    p = figure(width=400, height=400, x_range=x_range, x_axis_label=x_label, y_axis_label=y_label,
               toolbar_location=None, tools='hover', tooltips=tooltips, title=title)
    p.vbar(x=x, top=top, width=0.9, source=source)

    p.xaxis.major_label_orientation = pi/4
    p.y_range.start = 0

    return p


def create_circle_chart(source, x_range, x_label, y_label, title, tooltips, x, y):
    p = figure(width=400, height=400, x_range=x_range, x_axis_label=x_label, y_axis_label=y_label,
               toolbar_location=None, tools='hover', tooltips=tooltips, title=title)
    p.circle(x=x, y=y, width=5, source=source)

    p.yaxis[0].formatter = PrintfTickFormatter(format='%d億')
    p.xaxis.major_label_orientation = pi/4
    p.y_range.start = 0

    return p
