import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
from app import app

from models.subject import get_classes_by_term,CLASS_TERMS,EXAMS,get_all_grade_by_class_id,get_class_name
from apps.draw_mass import Mass,ClassInfo,static_header_trans
from apps.simple_chart import dash_table,dash_bar,find_nothing

ma = None

mass_layout = html.Div([
    html.Div(id = 'ma-total-selector', children = [
        html.Div(id = 'ma-select-term', children = [
            html.H3(children = '请选择学期:',style = {'display':'inline-block','margin-left':'10px','margin-right':'10px'}),
            html.Div(children = [
                dcc.Dropdown(
                    id = 'ma-term-selector',
                    options = [{'label':i,'value':i} for i in CLASS_TERMS],
                    value =CLASS_TERMS[0],
                    )
                ],style = {'display':'inline-block','width':'40%','vertical-align':'middle'})
            ]),
        html.Div(id = 'ma-select-grade'),
        ],className = 'one-row-con'
    ),
    
    

    html.Div(id = 'ma-means-show', children = [
        html.Div(children = [
            html.Div(id = 'ma-select-exam',style = {'display':'inline-block','margin-left':'10px','margin-right':'10px','width':'40%'}),
            html.Div(id = 'ma-select-subject',style = {'display':'inline-block','margin-left':'10px','margin-right':'10px','width':'40%'}),
        ], className = 'son-row-wrap'),
    ],className = 'one-row'),

    html.Div(id = 'ma-class-grade',children = [html.Img(id = 'chart-loading', src = './static/loading.gif')],className = 'one-row'),
    
    html.Div(id = 'ma-last-row',children = [
        html.Div(id = 'ma-inner-class',children = [
            html.Div(id = 'ma-select-class',style = {'display':'inline-block','margin':'10px','width':'40%'}),
            html.Div(id = 'ma-select-subject-innerclass',style = {'display':'inline-block','margin':'10px','width':'40%'}),
        ],className = 'son-row-wrap'),

        html.Div(id = 'ma-class-grade-rank',children = [html.Img(id = 'chart-loading', src = './static/loading.gif')],className = 'left-column'),
        html.Div(id = 'ma-class-grade-static',children = [html.Img(id = 'chart-loading', src = './static/loading.gif')],className = 'right-column'),
    ],className = 'one-row-wrap'),
])

@app.callback(
    Output('ma-select-grade','children'),
    [Input('ma-term-selector', 'value')]
)
def ma_select_term(term):
    data = get_classes_by_term(term)
    global ma
    ma = Mass(data) 
    grades = ma.get_grades()
    return [html.H3('请选择年级:',style = {'display':'inline-block','margin-left':'10px','margin-right':'10px'}),
        html.Div(children = [
             dcc.Dropdown(
                id = 'ma-grade-selector',
                options = [{'label':i,'value':i} for i in grades],
                value = grades[0],
            )
        ], style = {'display':'inline-block','width':'40%','vertical-align':'middle'})
   ]

@app.callback(
    Output('ma-select-exam','children'),
    [Input('ma-grade-selector','value')]
)
def ma_select_grade(grade):
    cla_id = ma.get_one_class_by_grade(grade)
    cla_info = ClassInfo(cla_id)
    exams = cla_info.get_exam()
    if not exams:
        return dcc.Dropdown(
                id = 'ma-exam-selector',
                options = [{'label':'此学期当前年级无考试记录','value':0}],
                value = 0
        )
    else:
        return dcc.Dropdown(
                id = 'ma-exam-selector',
                options = [{'label':EXAMS[i],'value':i} for i in exams],
                value = exams[0]
        )

@app.callback(
    Output('ma-select-subject','children'),
    [Input('ma-exam-selector','value')],
    [State('ma-grade-selector','value')]
)
def ma_gen_subject_select(exam,grade):
    cla_id = ma.get_one_class_by_grade(grade)
    cla_info = ClassInfo(cla_id)
    subjects = cla_info.get_exam_subjects(exam)
    subjects.append('总')

    if not exam:
        return dcc.Dropdown(
                id = 'ma-subject-selector',
                options = [{'label':'此学期当前年级无考试记录','value':0}],
                value = 0
        )
    else:
        return dcc.Dropdown(
                id = 'ma-subject-selector',
                options = [{'label':i,'value':i} for i in subjects],
                value = '总'
        )

@app.callback(
    Output('ma-class-grade','children'),
    [Input('ma-subject-selector','value')],
    [State('ma-grade-selector','value'),State('ma-exam-selector','value')]
)
def ma_select_subject(subject,grade,exam):
    if not subject or not exam:
        return find_nothing('此学期当前年级无考试记录')
            
    res = ma.get_mean_by_grade_exam(grade,exam,subject)
    res = res.sort_values('mean',ascending = False)
    res = res[['id','name','mean']]
    header = ['班级编号','班级名称',subject + '均分']
    return dash_table(header,res.T,'class-mean-by-exam-table',EXAMS[exam] + grade + '班级{0}平均分排名'.format(subject))


@app.callback(
    Output('ma-select-class','children'),
    [Input('ma-grade-selector','value')],
)
def ma_gen_class_select(grade):
    class_id = ma.get_class_by_grade_dict(grade)
    ids = list(class_id.keys())
    return dcc.Dropdown(
            id = 'ma-class-selector',
            options = [{'label':class_id[i],'value':i} for i in ids],
            value = ids[0]
    )

@app.callback(
    Output('ma-select-subject-innerclass','children'),
    [Input('ma-exam-selector','value')],
    [State('ma-grade-selector','value')]
)
def ma_select_subject_innerclass(exam,grade):
    cla_id = ma.get_one_class_by_grade(grade)
    cla_info = ClassInfo(cla_id)
    subjects = cla_info.get_exam_subjects(exam)
    subjects.append('总')
    return dcc.Dropdown(
            id = 'ma-subject-selector-innerclass',
            options = [{'label':i,'value':i} for i in subjects],
            value = '总'
    )

@app.callback(
    Output('ma-class-grade-rank','children'),
    [Input('ma-class-selector','value'),Input('ma-subject-selector-innerclass','value')],
    [State('ma-grade-selector','value'),State('ma-exam-selector','value')]
)
def ma_gen_rank(class_,subject,grade,exam):
    class_info = ClassInfo(class_)
    res =class_info.rank_grade(exam,subject)
    if res.empty:return find_nothing('此班级此次考试数据缺失')
    class_name = get_class_name(class_)
    res = res[['student_id','name','score','rank']]
    header = ['学号','姓名','分数','排名']
    return dash_table(header,res.T,'class-rank-by-exam-table','{0}{1}班{2}排名'.format(EXAMS[exam],class_name,subject))

@app.callback(
    Output('ma-class-grade-static','children'),
    [Input('ma-class-selector','value'),Input('ma-subject-selector-innerclass','value')],
    [State('ma-grade-selector','value'),State('ma-exam-selector','value')]
)
def ma_gen_ditribution(class_,subject,grade,exam):
    class_info = ClassInfo(class_)
    res =class_info.static_grade(exam,subject)
    if not res:return find_nothing('此班级此次考试数据缺失')
    class_name = get_class_name(class_)
    header,value = static_header_trans(res,exam)
    x_t = '分数段'
    y_t = '人数'
    title = '{0}{1}班{2}成绩分布'.format(EXAMS[exam],class_name,subject)
    id_ = 'ma-grade-bar-{0}'.format(class_)
    return dash_bar(header,value,x_t,y_t,id_,title)