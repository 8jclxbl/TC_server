import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd 
from app import app


#利用HTML制作的只有一行的表格
#接受的数据格式
#{'index'：表头信息，'value'：表中数据}
def simple_table(query_res):
    indexs = query_res['index']
    values = query_res['value']

    #作为图的一个下拉菜单来处理
    return html.Table(
        #表头
        [html.Tr([html.Th(index) for index in indexs])] + 
        #内容
        #html.Td如果输入的值为int0的话不会显示
        [html.Tr([html.Td(str(value)) for value in values])]
    ) 

def dash_table(head_val,value_val,tag_id):
    return dcc.Graph(
        id = tag_id,
        figure = {
            'data':[go.Table(
                header = dict(
                        values = ['<b>{0}</b>'.format(i) for i in head_val],
                        line = dict(color='white'),
                        fill = dict(color='#003472'),
                        align = ['left'] * 5,
                        font = {'color':'white'},
                        ),
                cells = dict(
                    values = value_val,
                    line = dict(color='white'),
                    fill = dict(color='#177cb0'),
                    align = ['left'] * 5,
                    font = {'color':'white'},
                    )
                )
            ]

        },
    )

    