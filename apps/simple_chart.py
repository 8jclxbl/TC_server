import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd 
from app import app


#利用HTML制作的只有一行的表格
#接受的数据格式
#{'index'：表头信息，'value'：表中数据}
def simple_table(query_res,title_):
    indexs = query_res['index']
    values = query_res['value']

    #作为图的一个下拉菜单来处理
    return html.Div(children = [
        html.H6(title_,style = {'text-align':'center'}),
        html.Table(
            #表头
            [html.Tr([html.Th(index) for index in indexs])] + 
            #内容
            #html.Td如果输入的值为int0的话不会显示
            [html.Tr([html.Td(str(value)) for value in values])]
        )
    ],style = {'margin-bottom':'10px'})

def find_nothing(content):
    return html.Div(
            id = 'cannot-find',
            children = [
                html.Img(src = './static/search-error.png',style = {'width':'150px','height':'150px'}),
                html.H5(content)
            ])

def text_return(content):
    return html.H3(children = content,style = {'top':' 50%','transform':' translateY(-50%)'})

def dash_table_predict(head_val,value_val,tab_id,title_name = '',predict = None):
    if predict:
        length = len(value_val[0])
        
        warning = predict[-1]

        if warning == 1:
            color_predict = '#d50000'
            text_ = '消费水平异常升高'
        elif warning == 2:
            color_predict = '#00c853'
            text_ = '消费水平不变'
        else:
            color_predict = '#880e4f'
            text_ = '消费水平异常降低'

        value_val[0] = list(value_val[0])
        value_val[1] = list(value_val[1])
        value_val[0].append(predict[0] + '消费预测,' + text_)
        value_val[1].append(predict[1] * -1)
        
        lcolor_ = ['white'] * (length + 1)
        color_ = ['#177cb0'] * length
        color_.append(color_predict)
    else:
        color_ = '#177cb0'
        lcolor_ = 'white'
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
                    line = dict(color=[lcolor_]),
                    fill = dict(color=[color_]),
                    align = ['left'] * 5,
                    font = {'color':'white'},
                    )
                )],
            'layout':go.Layout(
                    title = title_name,
                ),
        },
    )

def dash_table(head_val,value_val,tab_id,title_name = '',height_ = 450):
    return dcc.Graph(
        id = tab_id,
        figure = {
            'data':[go.Table(
                header = dict(
                        values = ['<b>{0}</b>'.format(i) for i in head_val],
                        line = dict(color='white'),
                        fill = dict(color='#003472'),
                        #align = ['left'] * 5,
                        font = {'color':'white'},
                        ),
                cells = dict(
                    values = value_val,
                    line = dict(color='white'),
                    fill = dict(color='#177cb0'),
                    #align = ['left'] * 5,
                    font = {'color':'white'},
                    ),
                )],
            'layout':go.Layout(
                    height = height_,
                    title = title_name,
                    margin = dict(b = 25,pad = 0)
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
                    plot_bgcolor="#dfe6e9",

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
    