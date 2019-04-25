import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
from app import app

from models.student import controller_info_by_student_id,pd_consumption_by_student_id,get_student_info_by_student_id
from apps.draw_controller import draw_controller_figure
from apps.draw_consumption import draw_consumption_figure,draw_consumption_table
from apps.draw_student import draw_student_table

colors = {     
    'background': '#111111',     
    'text': '#7FDBFF' 
}

total_layout = html.Div([
    html.H1(
        children = '忽然之间克哈的霓虹为我在闪烁', 
        style = {
            'textAlign':'center',
            'color':colors['text']
        }),

    dcc.Tabs(id='main-func-selector', value = 'welcome',children = [
        dcc.Tab(label = '欢迎', value = 'welcome' ),
        dcc.Tab(label = '学生域数据分析', value = 'student_analysis'),
        dcc.Tab(label = '课程域数据分析', value = 'subject_analysis'),
        dcc.Tab(label = '群体域数据分析', value = 'mass_analysis'),
        dcc.Tab(label = '其他', value = 'other'),
    ]),
    html.Div(id = 'sub-div')
    
])

sub_layout = [
    html.Div([
        html.H3(children = '数据筛选', style = {'color':colors['text']}),
        html.Div(id = 'data-select')
    ]),
    html.Div([
        html.H3(children = '绘图条件', style = {'color':colors['text']}),
        html.Div(id = 'plot-conditions')
    ]),
    dcc.Tabs(id='graph-table-selector', value = 'graph',children = [
        dcc.Tab(label = '图', value = 'graph' ),
        dcc.Tab(label = '数据表', value = 'table'),
    ]),

    html.Div(id = 'show-block')
]

student_layout = [
    html.Div(id = 'student_id',children = [
        html.H4(id = 'student-id-indicator',children = '请输入所要查询的学号'),
        dcc.Input(id='input-student-id', type='text', value='13012'),
        html.Button(children = '提交', id='student-id-submmit',n_clicks = 0), 
        html.Div(id = 'student-info') 
    ]),
    html.Div([
        html.H3(children = '绘图条件', style = {'color':colors['text']}),
        html.Div(id = 'plot-conditions')
    ]),
    dcc.Tabs(id='graph-table-selector', value = 'graph',children = [
        dcc.Tab(label = '图', value = 'graph' ),
        dcc.Tab(label = '数据表', value = 'table'),
    ]),
    html.Div(id = 'show-block'),
]

welcome_layout = [
    dcc.Markdown("""
# Welcome
---
> 忽然之间克哈的霓虹为我在闪烁
---
![welcome](./static/welcome.jpg "欢迎使用")
"""),
]

@app.callback(
    Output('sub-div','children'),
    [Input('main-func-selector','value')]
)
def main_func_selector(value):
    if value == 'welcome':
        return welcome_layout
    elif value  == 'student_analysis':
        return student_layout
    else:
        return sub_layout

#注意此处的参数位置和名称无关，只和Input的位置
@app.callback(
    Output('student-info', 'children'),
    [Input('student-id-submmit','n_clicks')],
    [State('input-student-id', 'value')],
)
def select_student(n_clicks,value):
    try:
        id = int(value)
        info = get_student_info_by_student_id(id)
        return draw_student_table(info)
    except ValueError:
        return "学号应该是纯数字"

@app.callback(
    Output('show-block','children'),
    [Input('graph-table-selector','value')]
)
def graph_table_selector(value):
    query_res = pd_consumption_by_student_id(14444)
    if value == 'graph':
        return draw_consumption_figure(query_res)
    else:
        return draw_consumption_table(query_res)
