import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
from app import app

from models.globaltotal import CLASS_TERMS,EXAMS,CLASS_HAS_DORM,CLASS_TABLE
from models.dorm import get_dorm_by_class_id,get_student_by_dorm_id
from models.student import get_student_info_by_student_id,consumption_by_student_id

from apps.draw_consumption import consumption_data_seperate,consumption_bar_dorm_month_compare
from apps.simple_chart import dash_table,find_nothing,simple_table
from apps.util import transpose

class_has_dorm = {i:CLASS_TABLE[i] for i in CLASS_HAS_DORM}

dorm_layout = html.Div([
    html.Div(id = 'dm-select-class',children = [
        html.Div(children = [
            html.H6('请选择班级:',style = {'display':'inline-block'}),
            html.Div(id = 'dm-select-class-container', children = [
                dcc.Dropdown(
                    id = 'dm-class-selector',
                    options = [{'label':j,'value':i} for i,j in class_has_dorm.items()],
                    value = CLASS_HAS_DORM[0]
                    )
            ],style = {'display':'inline-block','width':'40%','vertical-align':'middle','margin-left':'10px','margin-right':'10px'}),],style = {'display':'inline-block','width':'50%'}),
        
        html.Div(id = 'dm-select-class-dorm',style = {'display':'inline-block','width':'50%'})
    ],className = 'one-row'),
    html.Div(id = 'ma-info-show-table-container', children = [
        html.Div(id = 'ma-info-show-table',children = [html.Img(id = 'chart-loading', src = './static/loading.gif')],style = {'width':'98%','margin-left':'1%','margin-right':'1%'})
    ],className = 'one-row'),
    html.Div(id = 'ma-consumption-compare',children = [html.Img(id = 'chart-loading', src = './static/loading.gif')],className = 'one-row')
])


@app.callback(
    Output('dm-select-class-dorm','children'),
    [Input('dm-class-selector','value')]
)
def get_dorm_of_class(cla_id):
    dorms = get_dorm_by_class_id(cla_id)
    return [
        html.H6('请选择宿舍:',style = {'display':'inline-block'}),
        html.Div(children = [
                dcc.Dropdown(
                id = 'dm-class-dorm-selector',
                options = [{'label':i,'value':i} for i in dorms],
                value = dorms[0])
            ],style = {'display':'inline-block','width':'40%','vertical-align':'middle','margin-left':'10px','margin-right':'10px'}
        )
    ]

@app.callback(
    Output('ma-info-show-table','children'),
    [Input('dm-class-dorm-selector','value')],
    [State('dm-class-selector','value')]
)
def get_student_of_dorm(sushe_id,cla_id):
    students = get_student_by_dorm_id(sushe_id,cla_id)
    data = []
    index = ['学号','姓名','性别','民族','出生年份','家庭住址','家庭类型','政治面貌','班级','班级编号','班级学期','是否住校','是否退学','寝室号']
    for i in students:
        data.append(get_student_info_by_student_id(i)['value'])
    return dash_table(index,transpose(data),'dm-dorm-student-info','寝室{0}学生数据'.format(sushe_id),300,columnwidth_=[1,1,1,1,1,3,1,1,1,1,1,1,1,1])
    
@app.callback(
    Output('ma-consumption-compare','children'),
    [Input('dm-class-dorm-selector','value')],
     [State('dm-class-selector','value')]
)
def get_student_of_dorm(sushe_id,cla_id):
    students = get_student_by_dorm_id(sushe_id,cla_id)
    data = {}
    for i in students:
        query_res = consumption_by_student_id(i)
        if query_res['data'].empty:continue
        sumed = consumption_data_seperate(query_res,'Month')
        data[i] = {'data':sumed['data'],'predict':sumed['predict']}
    
    return consumption_bar_dorm_month_compare(data,sushe_id)