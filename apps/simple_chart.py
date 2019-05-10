import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go
import pandas as pd 
from app import app


#利用HTML制作的只有一行的表格
#接受的数据格式
#{'index'：表头信息，'value'：表中数据}

#此表格已支持多行
def simple_table(query_res,title_):
    indexs = query_res['index']
    values = query_res['value']

    #判断是否时单行表
    if isinstance(values[0],list):
        content = [html.Tr([html.Td(str(value)) for value in column]) for column in values]
    else:
        content = [html.Tr([html.Td(str(value)) for value in values])]

    #作为图的一个下拉菜单来处理
    return html.Div(children = [
        html.H6(title_,style = {'text-align':'center'}),
        html.Table(
            #表头
            [html.Tr([html.Th(index) for index in indexs])] + content
            #内容
            #html.Td如果输入的值为int0的话不会显示   
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

def dash_table(head_val,value_val,tab_id,title_name = '',height_ = 450,columnwidth_ = None):
    cols = len(head_val)
    if not columnwidth_: columnwidth_ = [1] * cols 

    return dcc.Graph(
        id = tab_id,
        figure = {
            'data':[go.Table(
                header = dict(
                        values = ['<b>{0}</b>'.format(i) for i in head_val],
                        line = dict(color='white'),
                        fill = dict(color='#003472'),
                        align=['center']*10,
                        font = {'color':'white'},
                        ),
                cells = dict(
                    values = value_val,
                    line = dict(color='white'),
                    fill = dict(color='#177cb0'),
                    align=['center']*10,
                    font = {'color':'white'},
                    ),
                columnwidth = columnwidth_,
                )],
            'layout':go.Layout(
                    height = height_,
                    title = title_name,
                    margin = dict(b = 25,pad = 0),
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


def dash_DropDown(id_,title_,option_label,option_value,default_value):
    return [
        html.H6(title_,style = {'display':'inline-block','width':'30%','margin-left':'10px','margin-right':'10px'}),
        html.Div(id = id_ + '-container',children = [
            dcc.Dropdown(
                id = id_,
                options = [{'label':i,'value':j} for i,j in zip(option_label,option_value)],
                value = default_value
            )
        ],style = {'display':'inline-block','width':'50%','margin-left':'10px','margin-right':'10px','vertical-align':'middle'})        
    ]
    
def dash_min_max_line(data,x_title,y_title,id_,title_name = ''):
    data = data.sort_values('exam_id')
    max_data = data['max']
    min_data = data['min']
    exams = data['exam']

    trace1 = go.Scatter(
        x = exams,
        y = max_data,
        name = '最高分',
        mode = 'lines+markers',
        marker = dict(
            symbol='circle',
            size = 10, 
            #color = color_value,
            #colorscale='Viridis',
            showscale=False,
            )
    )

    trace2 = go.Scatter(
        x = exams,
        y = min_data,
        name = '最低分',
        mode = 'lines+markers',
        marker = dict(
            symbol='circle',
            size = 10, 
            #color = color_value,
            #colorscale='Viridis',
            showscale=False,
            )
    )
    total = [trace1,trace2]
    return dcc.Graph(
            id = id_,
            figure = {
            'data':total,
            'layout': go.Layout(  
                    autosize=True,     
                    hovermode='closest',  
                    dragmode='select',     
                    title=title_name,
                    xaxis = dict(title = x_title, showline = True),
                    yaxis = dict(title = y_title, showline = True),
                    legend=dict(
                        font=dict(
                            size=10,
                        ),
                        yanchor='top',
                        xanchor='left',
                    ),
                    margin=dict(l=40,r=40,b=150,t=80),
                    
            )
            },
            style = {'align':'center','width':'80%','margin-left': '10%','margin-right': '10%'},
        )