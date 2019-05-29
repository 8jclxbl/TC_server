import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
from app import app

from models.globaltotal import CLASS_HAS_DORM,CLASS_TABLE
from models.dorm import get_dorm_by_class_id,get_student_by_dorm_id,get_grade_subjects 
from models.student import get_student_info_by_student_id,consumption_by_student_id

from apps.draw_consumption import consumption_data_seperate,consumption_bar_dorm_month_compare
from apps.simple_chart import dash_table,dash_DropDown
from apps.draw_dorm import DormGrade
from apps.util import transpose

ScoreType = {'score':'分数','t_score':'T值','z_score':'Z值','r_score':'等第'}
class_has_dorm = {i:CLASS_TABLE[i] for i in CLASS_HAS_DORM}

dorm_layout = html.Div([
    html.Div(id = 'dm-info-select-container',children = [
        html.Div(id = 'dm-student-info-title',children = [html.H4('宿舍学生基本信息',style = {'font-weight':'bold'})]),
        html.Hr(style = {'width':'90%'}),
        html.Div(id = 'dm-select-class',
            children = dash_DropDown('dm-class-selector','班级选择:',class_has_dorm.values(),class_has_dorm.keys(),list(class_has_dorm.keys())[0]),
            style = {'display':'inline-block','width':'50%'}),
        html.Div(id = 'dm-select-class-dorm',style = {'display':'inline-block','width':'50%'}),
        html.Div(id = 'dm-info-show-table',children = [html.Img(id = 'chart-loading', src = './static/loading.gif')])
    ],className = 'one-row'),
    
    html.Div(id = 'id-concumption-container', children = [
        html.Div(id = 'dm-student-info-title',children = [html.H4('宿舍学生消费对比',style = {'font-weight':'bold'})]),
        html.Hr(style = {'width':'90%'}),
        html.Div(id = 'dm-consumption-compare',children = [html.Img(id = 'chart-loading', src = './static/loading.gif')]),
    ],className ='one-row'),
    
    html.Div(id = 'dm-grade-container', children = [
        html.Div(id = 'dm-student-info-title',children = [html.H4('宿舍学生考试成绩对比',style = {'font-weight':'bold'})]),
        html.Hr(style = {'width':'90%'}),
        html.Div(id = 'dm-grade-selector-container', children = [
            html.Div(id='dm-select-subject',  style = {'display':'inline-block','width':'30%'}),
            html.Div(id='dm-select-exam-type', children = dash_DropDown('dm-exam-type-selector', '考试类型:', ['考试','平时成绩'],['normal','general'],'normal'), style = {'display':'inline-block','width':'30%'}),
            html.Div(id='dm-select-score-type', children = dash_DropDown('dm-score-type-selector', '分数类型:',list(ScoreType.values()),list(ScoreType.keys()),'r_score'),style = {'display':'inline-block','width':'30%'}),
        ], className = 'son-row-wrap'),
        html.Div(id = 'dm-grade-of-dorm', children = [html.Img(id = 'chart-loading', src = './static/loading.gif')])
    ],className = 'one-row'),
])


@app.callback(
    Output('dm-select-class-dorm','children'),
    [Input('dm-class-selector','value')]
)
def get_dorm_of_class(cla_id):
    dorms = get_dorm_by_class_id(cla_id)
    dorms.sort()
    return dash_DropDown('dm-class-dorm-selector','宿舍选择:',dorms,dorms,dorms[0])
   

@app.callback(
    Output('dm-info-show-table','children'),
    [Input('dm-class-dorm-selector','value')],
    [State('dm-class-selector','value')]
)
def get_student_of_dorm(sushe_id,cla_id):
    students = get_student_by_dorm_id(sushe_id,cla_id)
    data = []
    index = ['学号','姓名','性别','民族','出生年份','家庭住址','家庭类型','班级编号','班级名称','班级学期','政治面貌','是否住校','是否退学','寝室号']
    for i in students:
        data.append(get_student_info_by_student_id(i)['value'])
    return dash_table(index,transpose(data),'dm-dorm-student-info','{0}宿舍学生信息'.format(sushe_id),300,columnwidth_=[1,1,1,1,1,3,1,1,1,1,1,1,1,1])
    
@app.callback(
    Output('dm-consumption-compare','children'),
    [Input('dm-class-dorm-selector','value')],
    [State('dm-class-selector','value')]
)
def dorm_student_consumption_compare(sushe_id,cla_id):
    students = get_student_by_dorm_id(sushe_id,cla_id)
    data = {}
    for i in students:
        query_res = consumption_by_student_id(i)
        if query_res['data'].empty:continue
        sumed = consumption_data_seperate(query_res,'Month')
        data[i] = {'data':sumed['data'],'predict':sumed['predict']}
    
    return consumption_bar_dorm_month_compare(data,sushe_id)

@app.callback(
    Output('dm-select-subject', 'children'),
    [Input('dm-class-dorm-selector','value')],
    [State('dm-class-selector','value')]
)
def get_dorm_subjects(sushe_id, cla_id):
    subjects = get_grade_subjects(sushe_id,cla_id)
    labels = subjects['labels']
    #values = subjects['values']
    values = labels
    init_value = values[0]
    return dash_DropDown('dm-class-subject-selector','科目选择:',labels,values,init_value)

@app.callback(
    Output('dm-grade-of-dorm', 'children'),
    [Input('dm-exam-type-selector','value'),Input('dm-score-type-selector','value'),Input('dm-class-subject-selector','value')],
    [State('dm-class-dorm-selector','value'),State('dm-class-selector','value')]
)
def dorm_student_grade(exam_type,score_type,subject,sushe_id,cla_id):
    students = get_student_by_dorm_id(sushe_id,cla_id)
    dg = DormGrade(students,sushe_id)
    if exam_type == 'normal':is_noraml = True
    else: is_noraml = False
    return dg.seprate_by_subjects(subject,score_type,is_noraml)