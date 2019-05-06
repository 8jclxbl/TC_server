import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go 
from apps.simple_chart import dash_table

from app import app

CONTROLLER_COLOR = {100000:'#1A237E',100100:'#303F9F',100200:'#3F51B5',100300:'#7986CB',
                    200000:'#4A148C',200100:'#7B1FA2',200200:'#9C27B0',
                    300000:'#b71c1c',300100:'#d32f2f',300200:'#f44336',
                    9900100:'#1B5E20',9900200:'#388E3C',9900300:'#4CAF50',9900400:'#558B2F',9900500:'#7CB342'}

def controller_total(query_res,ctype,stu_id):
    data = query_res['data']
    table = query_res['type']
    stu_id = query_res['id']

    data['date'] = data['dates'].dt.date
    data['time'] = data['dates'].dt.time


    if ctype == 'graph':
        data = data[['date','time','types']]
        data_p = data_partation(data,table)
        chart = controller_graph(data_p,stu_id)
    else:
        data = data[['date','time','types']]
        header = ['日期','时间','类型']
        chart = controller_table(header,data.T)
    return chart

#根据考勤类型的不同建立一个色表
#色值开始为10
#每种之间差个20
def gen_color_value_map(type_table):
    colors = {}
    for i in type_table.keys():
        colors[i] = CONTROLLER_COLOR[i]
    return colors

#数据划分
#根据考勤不同的类型构造数据

#对于plotly图来说，如果要使用legend，就得分次画图，一次只画一类的数据点，所以要进行数据划分
def data_partation(data,table):
    colors = gen_color_value_map(table)
    dp_dic = {}

    for row in data.values:
        #当前类型
        cur_type = row[2]

        #原始数据处理，这里只是在测试的时候将就着用，具体使用的时候会根据orm模型的值来处理
        date = row[0]
        time = row[1]

        c_type = table[cur_type]
        color = colors[cur_type]
        desc = str(date) + ' ' + str(time) + ' ' + c_type

        #收录的数据意义如下
        #name:数据类型的名称，当前为考勤的类型
        #color:此类型对应的颜色
        #x,y:数据点
        #desc:每个数据点的详细信息
        if cur_type not in dp_dic:
            dp_dic[cur_type] = {'name':c_type,'color':color,'x':[date],'y':[time],'desc':[desc]}
        else:
            dp_dic[cur_type]['x'].append(date)
            dp_dic[cur_type]['y'].append(time)
            dp_dic[cur_type]['desc'].append(desc)
    return dp_dic

#绘制子图
def sub_scatter_bytype(name,color_value,x,y,text):
    return go.Scatter(
        x = x,
        y = y,
        name = name,
        mode = 'markers',
        text = text,
        marker = dict(
            symbol='circle',
            size = 8, 
            color = color_value,
            colorscale='Viridis',
            showscale=False,
            )
        )

def controller_graph(data_p,stu_id):
    total = []
    for i in data_p.values():
        total.append(sub_scatter_bytype(i['name'],i['color'],i['x'],i['y'],i['desc']))

    return dcc.Graph(
            id = 'student-controller',
            figure = {
            'data':total,
            'layout': go.Layout(  
                    #autosize=False,     
                    hovermode='closest',  
                    dragmode='select',     
                    title='学生{0}考勤记录统计'.format(stu_id),
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
            },
            style = {'align':'center','width':'80%','margin-left': '10%','margin-right': '10%'},
        )

def controller_table(head_val,value_val):
    return dash_table(head_val,value_val,'consumption-table')

def controller_rangeslider(data):
    terms = data['terms'].drop_duplicates().values
    length = len(terms)

    layout = dcc.RangeSlider(
            id = 'controller-range-slider',
            min=0,
            max=length,
            step=1,
            value=[0, length]),

    return layout