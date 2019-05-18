import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
from app import app

from models.globaltotal import CLASS_TERMS,THIRD_GRADE,CLASS_TABLE,ALL_CLASSES
from models.subject import class_grade_process,sql_73,get_all_grade_by_class_id_total
from apps.simple_chart import dash_table,dash_min_max_line,dash_DropDown
from apps.draw_eletive_subject import EletiveSubject

info = sql_73()
es = EletiveSubject(info)

subject_layout = html.Div([
    html.Div(id = 'sa-class-grade-title',children = [html.H4('班级历史得分趋势',style = {'font-weight':'bold'})],className = 'one-row'),
    
    html.Div(id= 'sa-class-term-select', children = [
        html.Div(id = 'sa-select-term',children = dash_DropDown('sa-term-selector','请选择要统计的学期:',CLASS_TERMS,CLASS_TERMS,CLASS_TERMS[0]),
        style = {'display':'inline-block','margin-left':'10px','margin-right':'10px','width':'40%'}),
        
        html.Div(id = 'sa-select-class-container',children = [
            html.Div(id = 'sa-select-class', style = {'display':'inline-block','margin-left':'10px','margin-right':'10px','width':'60%','vertical-align':'middle'})
        ],style = {'display':'inline-block','margin-left':'10px','margin-right':'10px','width':'40%'}),
    ],className = 'one-row'),
    
    html.Div(id = 'sa-class-grade-table',children = [html.Img(id = 'chart-loading', src = './static/loading.gif')],className = 'one-row'),

    html.Div(id = 'sa-select-subject-container',children = [
        html.Div(id = 'sa-select-subject',style = {'display':'inline-block','width':'30%','margin-left':'10px','vertical-align':'middle'})],className = 'one-row'),
    
    html.Div(id = 'sa-class-grade-graph',className = 'one-row'),

    html.Div(id = 'sa-73-title',children = [html.H4('2018-2019高三年级七选三状况统计',style = {'font-weight':'bold'})],className = 'one-row'),
    html.Div(id = 'total-73-statics', children = [
        html.Div(id = 'sa-73-show-up', children = [
            html.Div(id = 'sa-73-pie-total',className = 'left-column'),
            html.Div(id = 'sa-73-bar-total',className = 'right-column'),
        ],
        className = 'one-row-wrap'
        ),

        html.Div(id = 'sa-73-show-down',children = [
            html.Div(children = [
                html.Div(id = 'sa-73-select-class', children = dash_DropDown('sa-third-class-selector','请选择统计的班级：',THIRD_GRADE.values(),THIRD_GRADE.keys(),list(THIRD_GRADE.keys())[0]),className = 'one-row-con'),
                html.Div(id = 'sa-73-bar-class'),
            ],
            className = 'left-column'
            ),
            
            html.Div(id = 'sa-73-bar-subjecs-container',children = [
                html.Div(id = 'sa-third-select-combines',children = dash_DropDown('sa-subjects-selector','请选择统计的组合：',es.combines,es.combines,es.combines[0]),className = 'one-row-con'),
                html.Div(id = 'sa-73-bar-subjects'),
                ],
            className = 'right-column'
            ),
        ],
        className = 'one-row-wrap'
        )
    ])
    
])

@app.callback(
    Output('sa-select-class','children'),
    [Input('sa-term-selector', 'value')]
)
def select_term(term):
    df = ALL_CLASSES
    data = df.loc[df['class_term'] == term]
    ids = data['class_id'].values
    names = data['class_name'].values
    
    return dash_DropDown('sa-class-selector','请选择班级:',names,ids,ids[0])

@app.callback(
    Output('sa-select-subject','children'),
    [Input('sa-class-selector', 'value')]
)
def select_subject(class_):
    class_grade = get_all_grade_by_class_id_total(class_)
    if class_grade.empty:return '缺失此班学生的考试数据'
    subjects = class_grade['subject'].drop_duplicates().values  
    return dash_DropDown('sa-subject-selector','请选择课程:',subjects,subjects,subjects[0])

@app.callback(
    Output('sa-class-grade-table','children'),
    [Input('sa-class-selector', 'value')],
    [State('sa-term-selector', 'value')]
)
def grade_max_min_table(class_,term):
    class_grade = get_all_grade_by_class_id_total(class_)
    if class_grade.empty:return '缺失此班学生的考试数据'
    res = class_grade_process(class_grade)
    res = res[['subject','exam','max','min']]
    head = ['科目','考试','最高分','最低分']
    return dash_table(head,res.T,'calss-grade-statis-table',term + '学期' + CLASS_TABLE[class_] + '班成绩统计')

    
@app.callback(
    Output('sa-class-grade-graph','children'),
    [Input('sa-subject-selector','value')],
    [State('sa-class-selector', 'value')]
)
def max_min_graph(subject,class_):
    class_grade = get_all_grade_by_class_id_total(class_)
    if class_grade.empty:return '缺失此班学生的考试数据'
    res = class_grade_process(class_grade)
    data = res.loc[res['subject'] == subject]
    return dash_min_max_line(data,'考试名称','分数','sa-max-min-lines','{0}班{1}最高最低分分布'.format(CLASS_TABLE[class_],subject))


@app.callback(
    Output('sa-73-pie-total','children'),
    [Input('sa-third-class-selector','value')]
)
def show_total_pie(class_):
    return es.draw_total()
    
@app.callback(
    Output('sa-73-bar-total','children'),
    [Input('sa-third-class-selector','value')]
)
def show_one_subject_total(class_):
    return es.draw_by_one_subject()

@app.callback(
    Output('sa-73-bar-class','children'),
    [Input('sa-third-class-selector','value')]
)
def select_third_class(class_):
    return es.draw_by_class(class_)

@app.callback(
    Output('sa-73-bar-subjects','children'),
    [Input('sa-subjects-selector','value')]
)
def select_subject_combine(subjects):
    return es.draw_by_subjects(subjects)
