import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go 
from apps.simple_chart import dash_table

import pandas as pd
from app import app

from models.globaltotal import GENERE_EXAM_ID,SUBJECT_COLOR,SOCRE_TYPE_COLOR
from models.student import get_predict_rank

ScoreType = {'score':'分数','t_score':'T值','z_score':'Z值','r_score':'等第'}

#data_structure {subject_name:{type:{exam:score}}}
#绘制图中的一条线的函数
def draw_line(subject_name,type_name,data):
    return go.Scatter(
    
        x = data['head'],
        y = data['score'],
        #当前图的名称，亦即legend中的名称
        name = subject_name + ' ' + ScoreType[type_name],
        mode = 'lines+markers',

        #鼠标悬浮时显示的文字
        text = ['{0}{1}{2}:{3}'.format(k,subject_name,ScoreType[type_name],v) for k,v in zip(data['head'],data['score'])],
        
        #散点的属性
        marker = dict(
            symbol='circle',
            size = 8, 
            color = SUBJECT_COLOR[subject_name],
        ),
        
        #线的属性
        line = dict(
            color = SUBJECT_COLOR[subject_name],
        ),
        
        #如果两个散点之间有多个空缺数据，是否相连
        connectgaps=True
    )

#成绩类，用于处理学生的成绩，绘制学生的成绩图

class Grade:
    #query_res {'id':student_id,'data':学生成绩，type:pd.DataFrame}
    def __init__(self, query_res):
        
        self.student_id = query_res['id']
        #绘图时的图标题
        self.title = '学生{0}成绩'.format(self.student_id)
        self.data = query_res['data']

        self.other_types = {'Z值':'z_score','T值':'t_score','等第':'r_score'}
        
        self.separate_by_exam()
        self.separate_exam_genere()
        #self.info_each_exam()
        
        self.separate_by_subject()
        self.info_each_subject()
        #获取预测的分数
        self.predict_rank = get_predict_rank(self.student_id)
        
        #self.draw_all_lines()

    def gen_layout(self):
        layout = [
            html.Div(id = 'select-subject',children = [
                html.H6(children = '要显示的科目:',style = {'display':'inline-block','margin-right':'20px'}),
                html.Div(children = [
                    dcc.Dropdown(
                    id = 'grade-subject-selector',
                        options = [{'label':i,'value':i} for i in self.subjects],
                        value = ['语文','数学','英语'],
                        clearable = False,
                        multi=True,
                    )
                ],style = {'display':'inline-block','width':'70%'}),
            ]),
            html.Div(id = 'select-score-class',children = [
                html.Div(id = 'score-aspect-select',children = [
                    html.H6(children = '请选择评价方式:',style = {'display':'inline-block','margin-right':'20px'}),
                    dcc.RadioItems(
                        id = 'score-class-selector',
                        options = [
                            {'label':'分数','value':'origin'},
                            {'label':'评价指标','value':'others'}
                        ],
                        value = 'origin', 
                        labelStyle={'display': 'inline-block'},
                        style = {'display':'inline-block'},
                    ),
                    dcc.Dropdown(
                        id = 'grade-type-selector',
                        options = [{'label':k,'value':v} for k,v in self.other_types.items()],
                        value = list(self.other_types.values()),
                        clearable = False,
                        multi=True,
                    ),
                ],style = {'display':'inline-block'}),
                
            html.Div(id = 'score-select-exam-type', children = [
                html.H6(children = '请选择成绩类型:',style = {'display':'inline-block','margin-right':'20px'}),
                dcc.RadioItems(
                    id = 'score-exam-type-selector',
                    options = [
                        {'label':'平时成绩','value':'general'},
                        {'label':'考试','value':'exam'}
                    ],
                    value = 'exam', 
                    labelStyle={'display': 'inline-block'},
                    style = {'display':'inline-block'},
                    ),
                ]),
            ],style = {'display':'inline-block'}),
            
            html.Div(
                id = 'grade-graph',
                className = 'one-row',
            ),
        ]
        return layout

    def draw_all_lines(self):
        graph_cache = {}
        graph_cache_gen = {}
        score_type = ['score','z_score','t_score','r_score']
        data = self.grade_line_graph(self.subjects,score_type,True)
        data_gen = self.grade_line_graph(self.subjects,score_type,False)
        for i in self.subjects:
            cur_subject = data[i]
            cur_subject_gen = data_gen[i]
            temp = {}
            temp_gen = {}
            for j in score_type:
                cur_type = cur_subject[j]
                cur_type_gen = cur_subject_gen[j]
                temp[j] = draw_line(i,j,cur_type)
                temp_gen[j] = draw_line(i,j,cur_type_gen)
            graph_cache[i] = temp
            graph_cache_gen[i] = temp_gen
        self.graph_cache = graph_cache
        self.graph_cache_gen = graph_cache_gen

    def draw_line_total(self,subject_selected,type_selected,is_normal_exam):
        if is_normal_exam:
            cache = self.graph_cache
        else:
            cache = self.graph_cache_gen
        total = []
        if type_selected == 0:
            for subject in subject_selected:
                total.append(cache[subject]['score'])
        elif type_selected != []:
            for subject in subject_selected:
                for type_ in type_selected:
                    total.append(cache[subject][type_])
        else:
            total = []
        return dcc.Graph(
                id = 'student-grade-graph',
                figure = {
                'data':total,
                'layout': go.Layout(  
                        autosize=True,     
                        hovermode='closest',  
                        dragmode='select',     
                        title= self.title,
                        xaxis = dict(title = '考试', showline = True),
                        yaxis = dict(title = '分数', showline = True),
                        legend=dict(
                            font=dict(
                                size=10,
                            ),
                            yanchor='top',
                            xanchor='left',
                        ),
                        margin=dict(l=100,r=100,b=200,t=80),

                )
                },
                style = {'align':'center','width':'100%'},
            )

    def separate_by_exam(self):
        df = self.data
        self.exams = df['exam_name'].drop_duplicates().values
        self.exam_ids = df['exam_id'].drop_duplicates().values
        exam_dic = {}
        for i in self.exams:
            exam_dic[i] = df.loc[df['exam_name'] == i]

        self.grade_sep_by_exam = exam_dic

    def separate_exam_genere(self):
        exams = {}
        generes = {}
        length = len(self.exams)
        for i in range(length):
            if self.exam_ids[i] in GENERE_EXAM_ID:
                generes[self.exam_ids[i]] = self.exams[i]
            else:
                exams[self.exam_ids[i]] = self.exams[i]
        self.gen_exam = generes
        self.nor_exam = exams


    def separate_by_subject(self):
        df = self.data
        self.subjects = df['subject'].drop_duplicates().values
        self.subject_ids = df['subject_id'].drop_duplicates().values
        subject_dic = {}
        for i in self.subjects:
            subject_dic[i] = df.loc[df['subject'] == i]

        self.grade_sep_by_subject = subject_dic

    def info_each_subject(self):
        info = {}
        for i in self.subjects:
            info[i] = self.grade_sep_by_subject[i][['exam_id','exam_name','score','z_score','t_score','r_score']]
        self.grade_info_by_subject = info

    def get_exams(self):
        return self.exams

    def get_subjects(self):
        return self.subjects

    #获取某次考试各科的成绩
    def line_data_by_exam(self,exam_name,score_type):
        df = self.grade_sep_by_exam[exam_name]
        subject_name = df['subject'].values
        score = df[score_type].values

        return {'head':subject_name,'score':score}

    #获取某一门课各次考试的成绩
    def line_data_by_subject(self,subject,score_type,is_normal_exam):
        if is_normal_exam:
            exam_set = self.nor_exam
        else:
            exam_set = self.gen_exam
        df = self.grade_sep_by_subject[subject]

        exam_ids = df['exam_id'].values
        score = df[score_type].values

        exam_dic = {i:j for i,j in zip(exam_ids,score)}
        exam_set_sorted = sorted(list(exam_set.keys()))

        en = []
        sc = []
        for i in exam_set_sorted:
            en.append(exam_set[i])
            if i in exam_ids:
                sc.append(exam_dic[i])
            else:sc.append(None)
        if subject in self.predict_rank and score_type == 'r_score':
            en.append('下次考试等第预测')
            sc.append(self.predict_rank[subject])

        return {'head':en,'score':sc}

    def grade_line_graph(self,subject_selected,type_selected,is_normal_exam):
        total_data = {}
        for i in subject_selected:
            types_info = {}
            for j in type_selected:
                types_info[j] = self.line_data_by_subject(i,j,is_normal_exam)
            total_data[i] = types_info
        return total_data


    #由于将分数与其他的评价指标分开了，所以这里需要将这两个分数分开显示
    def line_data_by_subject_score(self,subject,is_normal_exam):
        return self.line_data_by_subject(subject,'score',is_normal_exam)

    def grade_line_graph_score(self,subject_selected,is_normal_exam):
        total_data = {}
        for i in subject_selected:
            total_data[i] = self.line_data_by_subject_score(i,is_normal_exam)
        return total_data