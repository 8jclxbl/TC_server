import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go

import pandas as pd 
from app import app
from apps.simple_chart import dash_table,dash_table_predict

from models.student import get_predict_consumption

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
    #data 格式为字典，其中的'data' 对应的是pandas.DataFrame
    #seq 是字符串，取值为'Total'，'Day'，'Month'，'Year'，分别对应，原始消费数据，按日划分，按月划分，按年划分
    info = data['data']
    predict = get_predict_consumption(data['id'])

    #用于填写表格标题，将sep转化为对应的汉语意义
    interval = title_table[sep]
    #最后输出的sumed是一个pandas.Series格式的数据，值为金额，index为聚合后的时间
    if sep == 'Total':      
        #输出原始数据时，金额不需要处理
        sumed = info['money']
        sumed.index = info['date'] + info['time']
    else:
        #将日期列的数据转化为datetime格式，便于后面的处理
        info['date'] = pd.to_datetime(info['date'])
        #选中Data列，基于sep来采样，
        # resample的参数只有一个字母，其意义和对应的意义sep一致，
        # 如sep为Day时，resample的参数为D，标识按照日跨度来重采样，最后根据采样结果求和
        sumed = info.set_index('date').resample(sep[0])['money'].sum()
        #部分时间区间的消费为0，直接删掉
        sumed = delete_selected_data_series(sumed,0)
        #由于金额时浮点数，所以需要舍入，取两位小数
        sumed = round(sumed,2)


        #根据sep组合时间区间
        if sep == 'Day':
            sumed.index = [str(i.year) +'-'+ str(i.month) + '-' + str(i.day) for i in sumed.index]
        elif sep == 'Month':
            last_ = sumed.index[-1]
            if last_.month == 12:
                last_month = 1
                last_year = int(last_.year) + 1
            else:
                last_year = int(last_.year)
                last_month = int(last_.month) + 1
            last_index = str(last_year) + '-' +str(last_month) 
            sumed.index = [str(i.year) +'-'+ str(i.month) for i in sumed.index]
            return {'data':sumed,'title_part':interval,'predict':[last_index,predict[0],predict[1]]}
            
        elif sep == 'Year':
            sumed.index = [i.year for i in sumed.index]

    return {'data':sumed,'title_part':interval}

def consumption_table_uds(sumed):
    data = sumed['data']
    interval = sumed['title_part']
    if interval != '月':predict = None
    else:predict = sumed['predict']
    return dash_table_predict(['时间','花费'],[data.index, data.values * -1],'consumption-table-by-interval','学生{0}消费统计表'.format(interval),predict)

def consumption_bar_uds(sumed):
    data = sumed['data']
    interval = sumed['title_part']
    
    total = [
        go.Bar(
            x = data.index,
            y = data.values * - 1,
            name = '学生消费',
        )
    ]
    if interval == '月':
        predict = sumed['predict']
        warning = predict[-1]

        if warning == 1:
            color_ = '#d50000'
            text_ = '消费水平异常升高'
        elif warning == 2:
            color_ = '#00c853'
            text_ = '消费水平不变'
        else:
            color_ = '#880e4f'
            text_ = '消费水平异常降低'
        total.append(
            go.Bar(x = [predict[0]],y = [-predict[1]],
                   text = ['该生下月消费预测,' + text_],
                   marker = dict(color = color_),name = '预测')
            )

    return dcc.Graph(
            id = 'consumption-graph-by-year-month',
            figure = {
                'data':total,
                'layout': go.Layout(    
                    hovermode='closest',  
                    dragmode='select',
                    plot_bgcolor="#dfe6e9",
                    title='学生{0}消费统计'.format(interval),
                    xaxis = dict(title = '时间', showline = True, tickangle = 75),
                    yaxis = dict(title = '花费', showline = True),
                    margin=dict(l=40,r=40,b=140,t=80),
                )
            },
            style = {'align':'center','width':'80%','margin-left': '10%','margin-right': '10%'},
        )

#{student_id{data,predict}}
def consumption_bar_dorm_month_compare(sumed,dorm_id):
    total = []
    for k,v in sumed.items():
        data = v['data']
        total.append(
            go.Bar(
                x = data.index,
                y = data.values * - 1,
                name = '学生{0}消费'.format(k),
            )
        )
    
        predict = v['predict']
        warning = predict[-1]

        if warning == 1:
            color_ = '#d50000'
            text_ = '消费水平异常升高'
        elif warning == 2:
            color_ = '#00c853'
            text_ = '消费水平不变'
        else:
            color_ = '#880e4f'
            text_ = '消费水平异常降低'
        total.append(
            go.Bar(x = [predict[0]],y = [-predict[1]],
                    text = ['该生下月消费预测,' + text_],
                    marker = dict(color = color_),name = '学生{0}预测'.format(k))
            )

    return dcc.Graph(
            id = 'consumption-graph-by-year-month',
            figure = {
                'data':total,
                'layout': go.Layout(    
                    hovermode='closest',  
                    dragmode='select',
                    plot_bgcolor="#dfe6e9",

                    title='{0}宿舍学生月消费统计'.format(dorm_id),
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

