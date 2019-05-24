import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
from app import app

from models.globaltotal import CLASS_TABLE,CLASS_YEARS,EXAMS
from models.subject import get_classes_by_year
from models.teacher import get_exams_by_year_grade,get_subject_by_year_grade_exam,get_grades_by_year_grade_subject
from apps.simple_chart import dash_table,dash_DropDown

teacher_layout = html.Div([
    html.Div(id = 'te-info-select-container-1',children = [
        html.Div(id = 'te-select-year',
            children = dash_DropDown('te-year-selector','请选择学年：',CLASS_YEARS,CLASS_YEARS,CLASS_YEARS[0]),style = {'display':'inline-block','width':'50%'}),
        html.Div(id = 'te-select-grade',style = {'display':'inline-block','width':'50%'}),
    ],className = 'one-row'),

    html.Div(id = 'te-info-select-container-2',children = [
        html.Div(id = 'te-select-exam',style = {'display':'inline-block','width':'50%'}),
        html.Div(id = 'te-select-subject',style = {'display':'inline-block','width':'50%'}),
    ],className = 'one-row'),

    html.Div(id = 'te-grade-show', className = 'one-row')
])


@app.callback(
    Output('te-select-grade','children'),
    [Input('te-year-selector','value')]
)
def te_get_grade(year):
    classes = get_classes_by_year(year)
    grades = classes['grade_name'].drop_duplicates().values
    grades = list(grades)
    if not grades:
        labels = ['缺失此学年的班级数据']
        values = [0]
        init_value = 0
    else:
        labels = grades
        values = grades
        init_value = values[0]
    return dash_DropDown('te-grade-selector','请选择年级:',labels,values,init_value)
   

@app.callback(
    Output('te-select-exam', 'children'),
    [Input('te-grade-selector','value')],
    [State('te-year-selector', 'value')]
)
def te_get_exams(grade,year):
    if not grade:
        labels = ['缺失此学年的班级数据']
        values = [0]
        init_value = 0
    else:
        exams = get_exams_by_year_grade(year,grade)
        labels = exams['labels']
        if not labels:
            labels = ['缺失此学年的班级数据']
            values = [0]
            init_value = 0
        else:
            values = exams['values']
            init_value = values[0]
    return dash_DropDown('te-exam-selector','请选择考试:',labels,values,init_value)

@app.callback(
    Output('te-select-subject', 'children'),
    [Input('te-exam-selector', 'value')],
    [State('te-year-selector','value'),State('te-grade-selector', 'value')]
)
def get_subject_of_year_exam(exam,year,grade):
    subject = get_subject_by_year_grade_exam(year,grade,exam)
    labels = subject['labels']
    if not labels:
        labels = ['缺失此此次考试的学科']
        values = [0]
        init_value = 0
    else:
        values = subject['values']
        init_value = values[0]
    return dash_DropDown('te-subject-selector','请选择考试:',labels,values,init_value)

@app.callback(
    Output('te-grade-show', 'children'),
    [Input('te-subject-selector', 'value')],
    [State('te-year-selector','value'),State('te-grade-selector', 'value'),State('te-exam-selector', 'value')]
)
def te_gen_chart(subject,year,grade,exam):
    data = get_grades_by_year_grade_subject(year, grade,exam,subject)
    print(data)
    return 'pass'
