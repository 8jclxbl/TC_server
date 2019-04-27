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
        [html.Tr([html.Td(value) for value in values])]
    ) 

    