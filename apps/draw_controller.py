import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go 
from app import app


#根据考勤类型的不同建立一个色表
#色值开始为10
#每种之间差个20
def gen_color_value_map(type_table):
    colors = {}
    count = 10
    for i in type_table.keys():
        colors[i] = count
        count += 20
    return colors

#数据划分
#根据考勤不同的类型构造数据

#对于plotly图来说，如果要使用legend，就得分次画图，一次只画一类的数据点，所以要进行数据划分
def data_partation(data,table):
    colors = gen_color_value_map(table)
    dp_dic = {}
    for i in data:
        #当前类型
        cur_type = i['type_id']

        #原始数据处理，这里只是在测试的时候将就着用，具体使用的时候会根据orm模型的值来处理
        d = i['date']
        t = i['time']
        h,m,s = t.split(':')
        h = int(h)
        m = float(m)/60
        tp = table[cur_type]
        cl = colors[cur_type]
        desc = d + ' ' + t + ' ' + tp

        #收录的数据意义如下
        #name:数据类型的名称，当前为考勤的类型
        #color:此类型对应的颜色
        #x,y:数据点
        #desc:每个数据点的详细信息
        if cur_type not in dp_dic:
            dp_dic[cur_type] = {'name':tp,'color':cl,'x':[d],'y':[h + m],'desc':[desc]}
        else:
            dp_dic[cur_type]['x'].append(d)
            dp_dic[cur_type]['y'].append(h+m)
            dp_dic[cur_type]['desc'].append(desc)
    return dp_dic

#绘制子图
def sep_scatter_by_type(name,color_value,x,y,text):
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

def draw_controller_figure(query_res):
    data = query_res['data']
    table = query_res['type']
    total = []
    data_p = data_partation(data,table)
    for i in data_p.values():
        total.append(sep_scatter_by_type(i['name'],i['color'],i['x'],i['y'],i['desc']))

    return dcc.Graph(
            id = 'my-heatmap',
            figure = {
                'data':total,
            'layout': go.Layout(  
                    autosize=False,     
                    hovermode='closest',  
                    dragmode='select',     
                    title='学生{0}考勤记录统计'.format('14444'),
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
                    paper_bgcolor='rgb(254, 247, 234)',
                    plot_bgcolor='rgb(254, 247, 234)',
                )
            }
        )
    