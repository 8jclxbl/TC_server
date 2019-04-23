import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input,Output
from app import app

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
    ])]

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
    else:
        return sub_layout