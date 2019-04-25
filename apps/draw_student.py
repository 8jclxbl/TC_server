import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd 
from app import app

def draw_student_table(query_res):
    index = query_res['index']
    value = query_res['value']

    #作为图的一个下拉菜单来处理
    max_rows = 10

    return dcc.Graph(
        id = 'student-info-table',
        figure = {
            'data':[go.Table(
                header = dict(
                        values = index,
                        line = dict(color='#7D7F80'),
                        fill = dict(color='#a1c3d1'),
                        align = ['left'] * 5),
                cells = dict(
                    values = value,
                    line = dict(color='#7D7F80'),
                    fill = dict(color='#EDFAFF'),
                    align = ['left'] * 5))
            ],

        }
    )