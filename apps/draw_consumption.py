import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go

import pandas as pd 
from app import app
from apps.simple_chart import dash_table

title_table = {'Year':'年','Month':'月','Day':'日','Total':'总'}
#前缀用于标识所分析的数据
#_uds后缀，支持上卷和下钻

#之后的所有新功能都按此方式命名，前缀标识所分析的数据，中缀为功能，后缀标识额外的功能

#整个文件只向外导出_total即可
def consumption_total(query_res,sep,ctype):
    sumed = consumption_data_seperate(query_res,sep)
    if ctype == 'graph':
        return consumption_bar_uds(sumed)
    else:
        return consumption_table_uds(sumed)

def delete_selected_data_series(data,val):
    need_del_bool = data.values != val
    return data[need_del_bool]

#按月和年份划分
def consumption_data_seperate(data, sep):
    info = data['data']
    
    if sep == 'Total':      
        sumed = info['money']
        sumed.index = info['date'] + info['time']
    else:
        info['date'] = pd.to_datetime(info['date'])
        sumed = info.set_index('date').resample(sep[0])['money'].sum()
        sumed = delete_selected_data_series(sumed,0)
        sumed = round(sumed,2)
        if sep == 'Day':
            sumed.index = [str(i.year) +'-'+ str(i.month) + '-' + str(i.day) for i in sumed.index]
        elif sep == 'Month':
            sumed.index = [str(i.year) +'-'+ str(i.month) for i in sumed.index]
        elif sep == 'Year':
            sumed.index = [i.year for i in sumed.index]

    interval = title_table[sep]
    
    return {'data':sumed,'title_part':interval}

def consumption_table_uds(sumed):
    data = sumed['data']
    #interval = sumed['title_part']
    return dash_table(['时间','花费'],[data.index, data.values * -1],'consumption-table-by-interval')

def consumption_bar_uds(sumed):
    data = sumed['data']
    interval = sumed['title_part']
    total = [
        go.Bar(
            x = data.index,
            y = data.values * - 1
        )
    ]

    return dcc.Graph(
            id = 'consumption-graph-by-year-month',
            figure = {
                'data':total,
                'layout': go.Layout(    
                    hovermode='closest',  
                    dragmode='select',
                    plot_bgcolor="#191A1A",

                    title='学生{0}消费统计'.format(interval),
                    xaxis = dict(title = '时间', showline = True, tickangle = 75),
                    yaxis = dict(title = '花费', showline = True),
                    margin=dict(l=40,r=40,b=140,t=80),
                )
            },
            style = {'align':'center','width':'80%','margin-left': '10%','margin-right': '10%'},
        )

def consumption_line_chart(query_res):
    data = query_res['data']
    text = query_res['text']
    x = data['date']
    y = data['money']
    
    total = [consumption_graph(x,y,text)]
    return dcc.Graph(
            id = 'student-consumption',
            figure = {
                'data':total,
                'layout': go.Layout(  
                    autosize=False,     
                    hovermode='closest',  
                    dragmode='select',     
                    title='学生{0}消费记录统计'.format(query_res['id']),
                    xaxis = dict(title = '日期', showline = True),
                    yaxis = dict(title = '时间', showline = True),
                    legend=dict(
                        font=dict(
                            size=10,
                        ),
                        yanchor='top',
                        xanchor='left',
                    ),
                    margin=dict(l=140,r=40,b=50,t=80),
                )
            }
        )

def consumption_graph(x,y,text):
    return go.Scatter(
        x = x,
        y = y,
        mode = 'lines+markers',
        text = text,
        marker = dict(
            symbol='circle',
            size = 8, 
            colorscale='Viridis',
            showscale=False,
            )
        )

