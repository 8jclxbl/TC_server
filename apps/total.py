import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
from app import app

from apps.student_page import student_layout
from apps.subject_page import subject_layout
from apps.mass_page import mass_layout

colors = {     
    'background': '#111111',     
    'text': '#7FDBFF' 
}

total_layout = html.Div([
    html.Div(
        className = 'app-title',
        children = [html.Span(
            children = ['忽然之间克哈的霓虹为我在闪烁'], 
            style = {'color':'#FFF','line-height':'60px','font-size':'40px','font-weight':'200','padding-left':'10px'},
        )],
        style = {'backgroundColor':'#7FDBFF','height':'60px'},
    ),

    dcc.Tabs(id='main-func-selector', value = 'welcome',children = [
        dcc.Tab(label = '欢迎', value = 'welcome' ),
        dcc.Tab(label = '学生域数据分析', value = 'student_analysis'),
        dcc.Tab(label = '课程域数据分析', value = 'subject_analysis'),
        dcc.Tab(label = '群体域数据分析', value = 'mass_analysis'),
    ]),
    html.Div(id = 'sub-div')
    
])


welcome_layout = [
    html.Div(id = 'welcome-div',children = [
    dcc.Markdown("""
# Welcome
---
忽然之间克哈的霓虹为我在闪烁
---
![welcome](./static/welcome.jpg "欢迎使用")
"""),
],className = 'one-row')
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
    elif value  == 'subject_analysis':
        return subject_layout
    elif value ==  'mass_analysis':
        return mass_layout