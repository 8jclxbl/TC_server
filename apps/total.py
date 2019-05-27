import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input,Output
from app import app

from apps.student_page import student_layout
from apps.subject_page import subject_layout
from apps.mass_page import mass_layout
from apps.dorm_page import dorm_layout
from apps.welcome_page import welcome_layout


total_layout = html.Div(id = 'total-content',children = [html.Div([
    html.Div(
            className = 'app-title',
            children = [
                html.Img(id = 'total_img', src = './static/background.jpg', style = {'width':'100%', 'height':'auto'},),
            ],
        ),

        dcc.Tabs(id='main-func-selector', value = 'welcome',className='custom-tabs-container',children = [
            dcc.Tab(label = '欢迎', value = 'welcome',className='custom-tab',selected_className='custom-tab--selected'),
            dcc.Tab(label = '学生域数据分析', value = 'student_analysis',className='custom-tab',selected_className='custom-tab--selected'),
            dcc.Tab(label = '课程域数据分析', value = 'subject_analysis',className='custom-tab',selected_className='custom-tab--selected'),
            dcc.Tab(label = '群体域数据分析', value = 'mass_analysis',className='custom-tab',selected_className='custom-tab--selected'),
            dcc.Tab(label = '宿舍域数据分析', value = 'dorm_analysis',className='custom-tab',selected_className='custom-tab--selected'),
        ]),
        html.Div(id = 'sub-div')
    ])],
)


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
    elif value == 'dorm_analysis':
        return dorm_layout
