import dash_html_components as html 
import dash_core_components as dcc
from dash.dependencies import Input,Output,State
from app import app

from models.subject import get_all_calsses,CLASS_TERMS,get_all_grade_by_class_id,class_grade_process,get_7_3,sql_73,get_class_name
from apps.simple_chart import dash_table
from apps.draw_eletive_subject import EletiveSubject

THIRD_GRADE = {916: '高三(02)',917: '高三(03)',918: '高三(04)',919: '高三(07)',920: '高三(08)',
               921: '高三(01)',922: '高三(05)',923: '高三(09)',924: '高三(06)',925: '高三(10)'}
info = sql_73()
es = EletiveSubject(info)

subject_layout = html.Div([
    html.Div(id= 'sa-class-term-select', children = [
        html.Div(id = 'sa-select-title',children = [html.H5('请选择要统计的班级及其所处学期：')],
                    style = {'display':'inline-block','width':'30%','margin-left':'10px','margin-right':'10px'}),
        html.Div(id = 'sa-select-term',children = [
                dcc.Dropdown(
                id = 'sa-term-selector',
                options = [{'label':i,'value':i} for i in CLASS_TERMS],
                value =CLASS_TERMS[0],
            ),
            ],style = {'display':'inline-block','width':'25%','margin-left':'10px','margin-right':'10px'}
        ),
        html.Div(id = 'sa-select-class',style = {'display':'inline-block','width':'25%','margin-left':'10px','margin-right':'10px'}),
    ],className = 'one-row-con'),
    
    html.Div(id = 'sa-class-grade',className = 'one-row'),

    html.Div(id = 'sa-73-title',children = [html.H5('2018-2019高三年级七选三状况统计')],className = 'one-row'),
    html.Div(id = 'total-73-statics', children = [
        html.Div(id = 'sa-73-show-up', children = [
            html.Div(id = 'sa-73-pie-total',className = 'left-column'),
            html.Div(id = 'sa-73-bar-total',className = 'right-column'),
        ],
        className = 'one-row-wrap'
        ),

        html.Div(id = 'sa-73-show-down',children = [
            html.Div(children = [
                html.Div(children = [
                    html.Div(html.Label('请选择统计的班级：'),style = {'font-size':'20px','display':'inline-block','width':'35%','margin-left':'10px','margin-right':'10px'}),
                    html.Div(dcc.Dropdown(
                        id = 'sa-third-class-selector',
                        options = [{'label':v,'value':k} for k,v in THIRD_GRADE.items()],
                        value = 921,
                        style = {'margin-top':'10px','margin-right':'10px','margin-left':'10px'}
                    ),style = {'display':'inline-block','width':'40%','margin-left':'10px','margin-right':'10px','vertical-align':'middle'}
                ),    
            ],className = 'one-row-con'),
                html.Div(id = 'sa-73-bar-class'),
            ],
            className = 'left-column'
            ),
            
            html.Div(id = 'sa-73-bar-subjecs-container',children = [
                html.Div(children = [
                    html.Div(html.Label('请选择统计的组合：'),style = {'font-size':'20px','display':'inline-block','width':'35%','margin-left':'10px','margin-right':'10px'}),
                    html.Div(dcc.Dropdown(
                        id = 'sa-subjects-selector',
                        options = [{'label':i,'value':i} for i in es.combines],
                        value =es.combines[0],
                    ),style = {'display':'inline-block','width':'40%','margin-left':'10px','margin-right':'10px','vertical-align':'middle'}
                ),
                ],className = 'one-row-con'),
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
    df = get_all_calsses()
    data = df.loc[df['term'] == term]
    names = data['name'].values
    ids = data['id'].values
    
    return dcc.Dropdown(
            id = 'sa-class-selector',
            options = [{'label':j,'value':i} for i,j in zip(ids,names)],
            value = ids[0],
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
    return dash_table(head,res.T,'calss-grade-statis-table',term + '学期' + get_class_name(class_) + '班成绩统计')


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