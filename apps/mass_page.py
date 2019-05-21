import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
from app import app

from models.globaltotal import CLASS_TERMS,EXAMS,CLASS_TABLE
from models.subject import get_classes_by_term
from apps.draw_mass import Mass,ClassInfo,static_header_trans,open_grade_sep,open_part_by_grade,get_a_class,dash_compare_bar
from apps.simple_chart import dash_table,dash_bar,find_nothing,dash_DropDown

ScoreType = {'score':'原始分','t_score':'标准分','div':'离均值'}
ma = None
grade_CLASS_TERMS = [i for i in CLASS_TERMS if i[-1] != '2']
grade_CLASS_TERMS.insert(1, '2013-2014-2')


mass_layout = html.Div([
    html.Div(id = 'ma-total-selector', children = [
        html.Div(children = [
            html.Div(id = 'ma-select-term', children = dash_DropDown('ma-term-selector','请选择学期:',grade_CLASS_TERMS,grade_CLASS_TERMS,grade_CLASS_TERMS[0]),style =  {'display':'inline-block','margin-left':'10px','margin-right':'10px','width':'40%'}),
            html.Div(id = 'ma-select-grade',style = {'display':'inline-block','margin-left':'10px','margin-right':'10px','width':'40%'}),
            ],className = 'son-row-wrap')
        ],className = 'one-row'),
    
    html.Div(id = 'ma-means-show', children = [
        html.Div(children = [

            html.Div(id = 'ma-select-exam',style = {'display':'inline-block','margin-left':'10px','margin-right':'10px','width':'40%'}),
            html.Div(id = 'ma-select-subject',style = {'display':'inline-block','margin-left':'10px','margin-right':'10px','width':'40%'}),

        ], className = 'son-row-wrap'),
    ],className = 'one-row'),

    html.Div(id = 'ma-class-grade',children = [html.Img(id = 'chart-loading', src = './static/loading.gif')],className = 'one-row'),
    html.Div(id = 'ma-distribute-compare',children = [html.Img(id = 'chart-loading', src = './static/loading.gif')],className = 'one-row'),
    
    html.Div(id = 'ma-last-row',children = [
        html.Div(id = 'ma-inner-class',children = [
            html.Div(id = 'ma-select-class',style = {'display':'inline-block','margin':'10px','width':'30%'}),
            html.Div(id = 'ma-select-subject-innerclass',style = {'display':'inline-block','margin':'10px','width':'30%'}),
            html.Div(id = 'ma-select-score-type',
                children = dash_DropDown('ma-score-type-selector','请选择分数类型:',ScoreType.values(),ScoreType.keys(),list(ScoreType.keys())[0]),
                style = {'display':'inline-block','margin':'10px','width':'30%'}),
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
    if data.empty:
        labels = ['当前学期无班级记录']
        values = [0]
        init_value = 0
    else:
        grades = open_grade_sep(data)
        if not grades:
            labels = ['当前学期无班级记录']
            values = [0]
            init_value = 0
        else:
            labels = grades
            values = grades
            init_value = grades[0]
        return dash_DropDown('ma-grade-selector','请选择年级:',labels,values,init_value)

@app.callback(
    Output('ma-select-exam','children'),
    [Input('ma-grade-selector','value')],
    [State('ma-term-selector','value')],
)
def ma_select_grade(grade,term):
    if not grade:
        labels = ['此学期无班级记录']
        values = [0]
        init_value = 0
    else:
        data = get_classes_by_term(term)
        global ma
        ma = Mass(data) 
        cla_id = ma.get_one_class_by_grade(grade)
        cla_info = ClassInfo(cla_id)
        exams = cla_info.get_exam()

        if not exams:
            labels = ['此学期当前年级无考试记录']
            values = [0]
            init_value = 0
        else:
            labels = [EXAMS[i] for i in exams]
            values = exams
            init_value = exams[0]

    return dash_DropDown('ma-exam-selector','请选择考试：',labels,values,init_value)
    

@app.callback(
    Output('ma-select-subject','children'),
    [Input('ma-exam-selector','value')],
    [State('ma-grade-selector','value')]
)
def ma_gen_subject_select(exam,grade):
    if not grade:
        labels = ['此学期无班级记录']
        values = [0]
        init_value = 0
    else:
        cla_id = ma.get_one_class_by_grade(grade)
        cla_info = ClassInfo(cla_id)
        subjects = cla_info.get_exam_subjects(exam)
        subjects.append('总')

        if not exam:
            labels = ['此学期当前年级无考试记录']
            values = [0]
            init_value = 0
            
        else:
            labels = subjects
            values = subjects
            init_value = subjects[0]
        
        return dash_DropDown('ma-subject-selector','请选择科目：',labels,values,init_value)

@app.callback(
    Output('ma-class-grade','children'),
    [Input('ma-subject-selector','value')],
    [State('ma-grade-selector','value'),State('ma-exam-selector','value')]
)
def ma_select_subject(subject,grade,exam):
    if not subject or not exam:return find_nothing('此学期当前年级无考试记录')
            
    res = ma.get_mean_by_grade_exam(grade,exam,subject)
    res = res.sort_values('mean',ascending = False)
    res['rank'] = range(1,len(res['mean'].values)+1)
    res = res[['id','name','mean','rank']]
    header = ['班级编号','班级名称',subject + '均分','排名']
    return dash_table(header,res.T,'class-mean-by-exam-table',EXAMS[exam] + grade + '班级{0}平均分排名'.format(subject),300)

@app.callback(
    Output('ma-distribute-compare','children'),
    [Input('ma-subject-selector','value')],
    [State('ma-grade-selector','value'),State('ma-exam-selector','value')]
)
def ma_gen_distribute_compare(subject,grade,exam):
    if not subject or not exam:return find_nothing('此学期当前年级无考试记录')
            
    res = ma.total_distribute_compare(grade,exam,subject)
    return dash_compare_bar(res,'成绩区间','人数','ma-distribute-compare-bar','{0}{1}{2}成绩分布比较'.format(EXAMS[exam],grade,subject))


@app.callback(
    Output('ma-select-class','children'),
    [Input('ma-grade-selector','value')],
    [State('ma-term-selector','value')]
)
def ma_gen_class_select(grade,term):
    if not grade:
        labels = ['此学期无班级记录']
        values = [0]
        init_value = 0
    else:
        data = get_classes_by_term(term)
        if data.empty:
            labels = ['此学期无班级记录']
            values = [0]
            init_value = 0
        else:
            grade_class = open_part_by_grade(data)
            class_id = grade_class[grade]
            
            class_ids = list(class_id.keys())
            class_names = [class_id[i] for i in class_ids]
            labels = class_names
            values = class_ids
            init_value = values[0]

    return dash_DropDown('ma-class-selector','请选择班级：',labels,values,init_value)
   

@app.callback(
    Output('ma-select-subject-innerclass','children'),
    [Input('ma-exam-selector','value')],
    [State('ma-grade-selector','value'),State('ma-term-selector','value')]
)
def ma_select_subject_innerclass(exam,grade,term):
    data = get_classes_by_term(term)
    cla_id = get_a_class(data,grade)
    cla_info = ClassInfo(cla_id)
    subjects = cla_info.get_exam_subjects(exam)
    subjects.append('总')
    return dash_DropDown('ma-subject-selector-innerclass','请选择课程：',subjects,subjects,subjects[-1])
    

@app.callback(
    Output('ma-class-grade-rank','children'),
    [Input('ma-class-selector','value'),Input('ma-subject-selector-innerclass','value'),Input('ma-score-type-selector','value')],
    [State('ma-grade-selector','value'),State('ma-exam-selector','value')]
)
def ma_gen_rank(class_,subject,score_type,grade,exam):
    class_info = ClassInfo(class_)
    res =class_info.rank_grade(exam,subject,score_type)
    if res.empty:return find_nothing('此班级此次考试数据缺失')
    res = res[['student_id','name',score_type,'rank']]
    header = ['学号','姓名','分数','排名']
    return dash_table(header,res.T,'class-rank-by-exam-table','{0}{1}班{2}{3}排名'.format(EXAMS[exam],CLASS_TABLE[class_],subject,ScoreType[score_type]))

@app.callback(
    Output('ma-class-grade-static','children'),
    [Input('ma-class-selector','value'),Input('ma-subject-selector-innerclass','value'),Input('ma-score-type-selector','value')],
    [State('ma-grade-selector','value'),State('ma-exam-selector','value')]
)
def ma_gen_ditribution(class_,subject,score_type,grade,exam):
    class_info = ClassInfo(class_)
    res =class_info.static_grade(exam,subject,score_type)

    if not res:return find_nothing('此班级此次考试数据缺失')

    header,value = static_header_trans(res,exam,score_type)
    x_t = '分数段'
    y_t = '人数'
    title = '{0}{1}班{2}{3}分布'.format(EXAMS[exam],CLASS_TABLE[class_],subject,ScoreType[score_type])
    id_ = 'ma-grade-bar-{0}'.format(class_)
    
    return dash_bar(header,value,x_t,y_t,id_,title)