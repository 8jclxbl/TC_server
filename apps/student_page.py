import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
from app import app

from models.student import controller_info_by_student_id,consumption_by_student_id,get_student_info_by_student_id,get_grad_student_info_by_student_id,get_teachers_by_class_id,grade_query_res

from apps.draw_controller import controller_total
from apps.draw_consumption import consumption_total
from apps.draw_controller_statics import controller_statics_total,controller_statics
from apps.draw_grade import Grade
from apps.simple_chart import simple_table,dash_table,find_nothing

student_layout = [
    html.Div(id = 'student-id',children = [
        html.H4(
            id = 'student-id-indicator',
            children = '请输入所要查询的学号: ',
            style = {'display': 'inline-block','margin-right':'10px'}),
        dcc.Input(
            id='input-student-id', 
            type='text', 
            value='14567',
            style = {'display': 'inline-block','margin-left':'10px','margin-right':'10px'}),
        html.Button(
            children = '提交', 
            id='student-id-submmit',
            n_clicks = 0,
            style={"height": "34","background": "#119DFF","border": "1px solid #119DFF","color": "white",'margin-left':'10px','margin-right':'10px'}), 
        html.Div(id = 'student-info',style = {'padding-bottom':'10px'}),
        ],
        className = 'one-row',
    ),
    html.Div(id = 'student-grade',children = [html.Img(id = 'chart-loading', src = './static/loading.gif')],className = 'one-row'),
    html.Div(id = 'grade-lines',children = [html.Img(id = 'chart-loading', src = './static/loading.gif')],className = 'one-row'),

    html.Div(id = 'student-controller-total', children = [
        html.Div(children = [
            html.H6('学生考勤状况统计:',style = {'margin-left':'10px','margin-right':'10px'}),
        ],style = {'width':'20%','display':'inline-block'}),
        html.Div(id = 'controller-select-aspect',children = [
            dcc.Dropdown( 
                id = 'controller-aspect-selector',
                options=[            
                    {'label': '学生考勤情况', 'value': 'controller'},
                    {'label': '学生考勤统计', 'value': 'controller-st'},                  
                ],         
                value='controller',  
                clearable=False,       
            ),
        ],style = {'width':'30%','display':'inline-block'}),

        html.Div(id = 'controller-select-chart',children = [
            dcc.Dropdown( 
                id = 'controller-graph-table-selector',
                options=[            
                        {'label': '统计图', 'value': 'graph'},             
                        {'label': '统计表', 'value': 'table'},             
                ],         
                value='graph', 
                clearable=False,     
                ),
        ],style = {'width':'30%','display':'inline-block','margin-left':'10px'}),  

    ],className = 'one-row-con'),

    html.Div(id = 'student-controller-show', className = 'one-row'),

    html.Div(id = 'student-consumption-total',children = [
        html.Div(children = [
            html.H6('学生消费状况统计',style = {'margin-left':'10px','margin-right':'10px'})
        ],style = {'width':'20%','display':'inline-block'}),
        html.Div(id = 'consumption-select-chart',children = [
            dcc.Dropdown( 
                id = 'consumption-graph-table-selector',
                options=[            
                    {'label': '统计图', 'value': 'graph'},             
                    {'label': '统计表', 'value': 'table'},             
                ],         
                value='graph', 
                clearable=False,     
            ),  
        ],style={'width':'30%','display': 'inline-block','margin-left':'10px','margin-right':'10px'}),     
        html.Div(id = 'stua-select-interval', children = [
            dcc.Dropdown( 
                id = 'interval-selector',
                options=[            
                    {'label': '年数据', 'value': 'Year'},             
                    {'label': '月数据', 'value': 'Month'},  
                    {'label': '日数据', 'value': 'Day'},   
                    {'label': '总数据', 'value': 'Total'}        
                ],         
                value='Day',    
                clearable=False,     
            ),
        ],style={'width':'30%','display': 'inline-block','margin-left':'10px','margin-right':'10px'},), 
    ],className = 'one-row-con'),
    html.Div(id = 'student-consumption-show', className = 'one-row'),
]
#注意此处的参数位置和名称无关，只和Input的位置
@app.callback(
    Output('student-info', 'children'),
    [Input('student-id-submmit','n_clicks'),Input('input-student-id', 'value')],
)
def select_student(n_clicks,value):
    is_grad = False
    try:
        stu_id = int(value)
        try:
            info = get_student_info_by_student_id(stu_id)
        except AttributeError:
            try:
                info = get_grad_student_info_by_student_id(stu_id)
                is_grad = True
            except AttributeError:
                return "此学生的部分信息有缺失"

        student_infos = simple_table(info,'学生{0}基本信息'.format(stu_id))
        if is_grad:
            return [student_infos]

        class_id = info['value'][9]
        teachers = get_teachers_by_class_id(class_id)
        student_teachers = simple_table(teachers,'学生{0}各科教师'.format(stu_id))
        return [student_infos,student_teachers]
    except ValueError:
        return "学号应该是纯数字"

@app.callback(
    Output('student-grade', 'children'),
    [Input('student-id-submmit','n_clicks')],
    [State('input-student-id', 'value')]
)
def student_grade(n_clicks,stu_id):
    grade = grade_query_res(stu_id)['data']
    if grade.empty:return find_nothing('缺失该学生的考试数据')
    header = ['考试名称','科目','分数','Z值','T值','等第']
    grade = grade[['exam_name','subject','score','z_score','t_score','r_score']]
    return dash_table(header,grade.T,'student-grade-table','学生{0}历次考试成绩统计表'.format(stu_id))

@app.callback(
    Output('grade-lines', 'children'),
    [Input('student-id-submmit','n_clicks')],
    [State('input-student-id', 'value')]
)
def student_grade_graph_layout(n_clicks,stu_id):
    grade = grade_query_res(stu_id)
    if grade['data'].empty:return find_nothing('缺失该学生的考试数据')
    gd = Grade(grade)
    return gd.gen_layout()

@app.callback(
    Output('grade-graph', 'children'),
    [Input('grade-subject-selector','value'),Input('score-class-selector','value'),Input('grade-type-selector','value'),Input('score-exam-type-selector','value')],
    [State('input-student-id', 'value')]
)
def student_grade_graph(subjects,score_type,score_types,is_nor_exam,stu_id):
    grade = grade_query_res(stu_id)
    if grade['data'].empty:return find_nothing('缺失该学生的考试数据')
    gd = Grade(grade)
    gd.draw_all_lines()
    if score_type == 'origin':
        return gd.draw_line_total(subjects,0,is_nor_exam)
    else:
        return gd.draw_line_total(subjects,score_types,is_nor_exam)

@app.callback(
    Output('student-controller-show','children'),
    [Input('controller-aspect-selector','value'),Input('controller-graph-table-selector','value'),Input('input-student-id', 'value')],
)
def controller_selector(aspect,graph_table,stu_id):
    query_res = controller_info_by_student_id(stu_id)
    #The truth value of a DataFrame is ambiguous. Use a.empty, a.bool(), a.item(), a.any() or a.all().
    if query_res['data'].empty:return find_nothing('缺失该学生的考勤数据')
    if aspect == 'controller':
        return controller_total(query_res,graph_table,stu_id)
    else:
        cs = controller_statics(query_res)
        return cs.gen_layout()

@app.callback(
    Output('student-consumption-show','children'),
    [Input('consumption-graph-table-selector','value'),Input('interval-selector','value'),Input('input-student-id', 'value')],
)
def consumption_selector(graph_table,intervel,stu_id):
    query_res = consumption_by_student_id(stu_id)
    if query_res['data'].empty:return find_nothing('缺失该学生的消费数据')
    return consumption_total(query_res,intervel,graph_table)

@app.callback(
    Output('controller-select-chart','style'),
    [Input('controller-aspect-selector','value')]
)
def graph_table_lantent(aspect):
    if aspect == 'controller-st' :
       return {'display':'None'}
    else:
        return {'width':'30%','display':'inline-block','margin-left':'10px','margin-right':'10px'}


@app.callback(
    Output('controller-statics','children'),
    [Input('term-selector','value'),Input('input-student-id', 'value')]
)
def term_selector(term,stu_id):
    query_res = controller_info_by_student_id(stu_id)
    if query_res['data'].empty:return find_nothing('缺失该学生的考勤数据')
    cs = controller_statics(query_res)
    info = cs.pie_data(term)
    title = cs.title
    table_data = {'index':['出勤','迟到早退','请假'],'value':info}
    return [controller_statics_total(info,term,title),simple_table(table_data,'学生{0}{1}学期出勤情况统计'.format(stu_id,term))]


@app.callback(
    Output('grade-type-selector','style'),
    [Input('score-class-selector','value')]
)
def score_type_latent(score_type):
    if score_type == 'origin' :
        return {'display':'None'}
    else:
        return {'width':'311px','display':'inline-block','margin-left':'20px'}