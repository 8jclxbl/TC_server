import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd 
from app import app

def draw_consumption_graph(query_res):
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
                    #paper_bgcolor='rgb(254, 247, 234)',
                    #plot_bgcolor='rgb(254, 247, 234)',
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

def draw_consumption_table(query_res):
    data = query_res['data']
    id = query_res['id']

    #作为图的一个下拉菜单来处理
    max_rows = 10

    return dcc.Graph(
        id = 'consumption-table',
        figure = {
            'data':[go.Table(
                header = dict(
                        values = data.columns,
                        line = dict(color='#7D7F80'),
                        fill = dict(color='#a1c3d1'),
                        align = ['left'] * 5),
                cells = dict(
                    values = [data[i] for i in data.columns],
                    line = dict(color='#7D7F80'),
                    fill = dict(color='#EDFAFF'),
                    align = ['left'] * 5))
            ]
            
            #'layout':go.Layout(
            #    width=500, 
            #    height=300)
        }
    )