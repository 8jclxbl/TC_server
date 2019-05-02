import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
from app import app

from models.subject import get_all_calsses,CLASS_TERMS,get_all_grade_by_class_id,class_grade_process
from apps.simple_chart import dash_table

class_grade = None

subject_layout = html.Div([
    dcc.Dropdown(
        id = 'sa-term-selector',
        options = [{'label':i,'value':i} for i in CLASS_TERMS],
        value =CLASS_TERMS[0]
    ),
    html.Div(id = 'sa-select-class'),
    html.Div(id = 'sa-select-subject'),
    html.Div(id = 'sa-class-grade')
])

@app.callback(
    Output('sa-select-class','children'),
    [Input('sa-term-selector', 'value')]
)
def select_term(term):
    df = get_all_calsses()
    data = df.loc[df['term'] == term]
    names = data['name'].values
    ids = data['id'].values
    
    return dcc.Dropdown(
            id = 'sa-class-selector',
            options = [{'label':j,'value':i} for i,j in zip(ids,names)],
        )


@app.callback(
    Output('sa-class-grade','children'),
    [Input('sa-class-selector', 'value')]
)
def select_subject(class_):
    class_grade = get_all_grade_by_class_id(class_)
    res = class_grade_process(class_grade)
    res = res[['subject','exam','max','min']]
    head = ['科目','考试','最高分','最低分']
    return dash_table(head,res.T,'calss-grade-statis-table')
    
   


"""
@app.callback(
    Output('sa-class-grade','children'),
    [Input('sa-class-selector', 'value')]
)
def select_class(class_):
    df = get_all_grade_by_class_id(class_)
    head = ['学号','姓名','考试编号','学科','分数','Z值','T值','等第']
    df = df[['student_id','name','exam_id','subject','score','z_score','t_score','r_score']]
    return dash_table(head,df.T,'class_grade_table')
"""