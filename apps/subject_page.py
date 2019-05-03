import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
from app import app

from models.subject import get_all_calsses,CLASS_TERMS,CURRENT_THIRD,get_all_grade_by_class_id,class_grade_process,get_7_3,get_7_3_by_df,gen_all_table
from apps.simple_chart import dash_table

subject_layout = html.Div([
    dcc.Dropdown(
        id = 'sa-term-selector',
        options = [{'label':i,'value':i} for i in CLASS_TERMS],
        value =CLASS_TERMS[0]
    ),
    html.Div(id = 'sa-select-class'),
    html.Div(id = 'sa-select-subject'),
    html.Div(id = 'sa-class-grade'),

    dcc.Dropdown(
        id = 'sa-third-class-selector',
        options = [{'label':i,'value':i} for i in CURRENT_THIRD],
        value =CURRENT_THIRD[0]
    ),
    html.Div(id = 'sa-7-3-show')
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
    [Input('sa-class-selector', 'value')],
    [State('sa-term-selector', 'value')]
)
def select_subject(class_,term):
    class_grade = get_all_grade_by_class_id(class_)
    if class_grade.empty:return '缺失此班学生的考试数据'
    res = class_grade_process(class_grade)
    res = res[['subject','exam','max','min']]
    head = ['科目','考试','最高分','最低分']
    return dash_table(head,res.T,'calss-grade-statis-table',term + '学期' + str(class_) + '班成绩统计')
    

"""
@app.callback(
    Output('sa-7-3-show','children'),
    [Input('sa-third-class-selector','value')]
)
def select_third_class(class_):
    class_grade = get_all_grade_by_class_id(class_)
    info = get_7_3_by_df(class_grade,class_)
    info = info[['student_id','student_name','class_id','subject']]
    head = ['学号','姓名','班级id','科目']
    return dash_table(head,info.T,'class-7-3-table',str(class_))


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