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

def find_nothing(content):
    return html.Div(
            id = 'cannot-find',
            children = [
                html.Img(src = './static/search_error.png',style = {'width':'150px','height':'150px'}),
                html.H5(content)
            ])

def text_return(content):
    return html.H3(children = content,style = {'top':' 50%','transform':' translateY(-50%)'})

def dash_table(head_val,value_val,tab_id,title_name = ''):
    return dcc.Graph(
        id = tab_id,
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
                )],
            'layout':go.Layout(
                    title = title_name,
                ),
        },
    )

def dash_bar(head_val,value_val,x_title,y_title,tab_id,title_name = ''):
    total = [
            go.Bar(
                x = head_val,
                y = value_val,
            )
        ]

    return dcc.Graph(
            id = tab_id,
            figure = {
                'data':total,
                'layout': go.Layout(    
                    hovermode='closest',  
                    dragmode='select',
                    plot_bgcolor="#191A1A",

                    title=title_name,
                    xaxis = dict(title = x_title, showline = True, tickangle = 75),
                    yaxis = dict(title = y_title, showline = True),
                    margin=dict(l=40,r=40,b=140,t=80),
                )
            },
               
        )

def dash_DropDown(id_,option_label,option_value,default_value):
    return dcc.Dropdown(
        id = id_,
        options = [{'label':i,'value':j} for i,j in zip(option_label,option_value)],
        value = default_value
    )
    