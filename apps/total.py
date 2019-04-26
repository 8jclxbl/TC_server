import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
from app import app

from models.student import controller_info_by_student_id,consumption_by_student_id,get_student_info_by_student_id,get_teachers_by_class_id
from apps.draw_controller import controller_total
from apps.draw_consumption import consumption_total
from apps.draw_student import draw_student_table,draw_student_teachers

colors = {     
    'background': '#111111',     
    'text': '#7FDBFF' 
}

total_layout = html.Div([
    html.Div(
        children = '忽然之间克哈的霓虹为我在闪烁', className = 'app-title'
    ),

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
    html.Div(id = 'show'),
]

student_layout = [
    html.Div(id = 'student-id',children = [
        html.H4(
            id = 'student-id-indicator',
            children = '请输入所要查询的学号',
            style = {'display': 'inline-block'}),
        dcc.Input(
            id='input-student-id', 
            type='text', 
            value='13012',
            style = {'display': 'inline-block'}),
        html.Button(
            children = '提交', 
            id='student-id-submmit',
            n_clicks = 0,
            style={
                "height": "34",
                "background": "#119DFF",
                "border": "1px solid #119DFF",
                "color": "white"}), 
        html.Div(id = 'student-info'),
    ]),
    html.Div([
        html.H3(children = '绘图条件', style = {'color':colors['text']}),
        html.Div(id = 'plot-conditions', children = [
            dcc.Dropdown( 
                id = 'aspect-selector',
                options=[            
                    {'label': '学生考勤情况', 'value': 'controller'},             
                    {'label': '学生消费情况', 'value': 'consumption'},             
                   ],         
                value='controller',  
                style={'width': '20%', 'display': 'inline-block'},
                clearable=False,       
            ), 

            dcc.Dropdown( 
                id = 'month-year-selector',
                options=[            
                    {'label': '年度数据', 'value': 'Year'},             
                    {'label': '月度数据', 'value': 'Month'},  
                    {'label': '总体数据', 'value': 'total'},           
                   ],         
                value='total',    
                style={'width': '20%', 'display': 'inline-block'},
                clearable=False,     
            ), 

            dcc.Dropdown( 
                id = 'graph-table-selector',
                options=[            
                    {'label': '统计图', 'value': 'graph'},             
                    {'label': '统计表', 'value': 'table'},             
                ],         
                value='graph', 
                style={'width': '20%', 'display': 'inline-block'},
                clearable=False,         
            ), 
        ]),
    ]),
    html.Div(id ='student-show'),
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
    [State('input-student-id', 'value')]
)
def select_student(n_clicks,value):
    try:
        id = int(value)
        try:
            info = get_student_info_by_student_id(id)
        except AttributeError:
            return "此学生的部分信息有缺失"

        class_id = info['value'][9]
        teachers = get_teachers_by_class_id(class_id)
        student_infos = draw_student_table(info)
        student_teachers = draw_student_teachers(teachers)
        return [student_infos,student_teachers]
    except ValueError:
        return "学号应该是纯数字"

@app.callback(
    Output('student-show','children'),
    [Input('aspect-selector','value'),Input('graph-table-selector','value'),Input('month-year-selector','value')],
    [State('input-student-id', 'value')]
)
def graph_table_selector(aspect,graph_table,month_year,stu_id):
    if aspect == 'controller':
        query_res = controller_info_by_student_id(stu_id)
        if not query_res['data']:return '缺失该学生的考勤数据'
        return controller_total(query_res,graph_table)
    else:
        query_res = consumption_by_student_id(stu_id)
        if query_res['data'].empty:return '缺失该学生的消费数据'
        return consumption_total(query_res,month_year,graph_table)