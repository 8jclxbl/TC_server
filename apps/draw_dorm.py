import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go

from apps.simple_chart import dash_table
from apps.draw_grade import Grade

import pandas as pd
from app import app

from models.globaltotal import GENERE_EXAM_ID,SUBJECT_COLOR,SOCRE_TYPE_COLOR,TRADITION_COLOR_MAP
from models.student import grade_query_res,get_predict_rank,grade_query_res
from models.dorm import get_student_by_dorm_id

ScoreType = {'score':'分数','t_score':'T值','z_score':'Z值','r_score':'等第'}

#data_structure {subject_name:{type:{exam:score}}}
#绘制图中的一条线的函数
def dorm_draw_line(subject_name,type_name,data,order):
    student_id = data['student_id']
    return go.Scatter(
        x = data['head'],
        y = data['score'],
        #当前图的名称，亦即legend中的名称
        name = str(student_id)  + ' ' + subject_name + ' ' + ScoreType[type_name],
        mode = 'lines+markers',

        #鼠标悬浮时显示的文字
        text = ['{0}{1}{2}:{3}'.format(k,subject_name,ScoreType[type_name],v) for k,v in zip(data['head'],data['score'])],
        
        #散点的属性
        marker = dict(
            symbol='circle',
            size = 8, 
            color = TRADITION_COLOR_MAP[order],
        ),
        
        #线的属性
        line = dict(
            color = TRADITION_COLOR_MAP[order],
        ),
        
        #如果两个散点之间有多个空缺数据，是否相连
        connectgaps=True
    )


class DormGrade:
    def __init__(self,student_ids, sushe_id):
        self.student_ids = student_ids
        self.sushe_id = sushe_id
        self.grade_objs = [Grade(grade_query_res(i)) for i in student_ids]

    #为了保持简洁性，这里宿舍成绩对比只显示单科成绩
    def seprate_by_subjects(self,subject, score_type, is_normal_exam):
        total = []
        order = 0
        for obj in self.grade_objs:
            data = obj.line_data_by_subject(subject,score_type,is_normal_exam)
            if not data:continue
            data['student_id'] = obj.student_id
            total.append(dorm_draw_line(subject, score_type, data,order))
            order += 3
        return dcc.Graph(
            id = 'dorm-student-grade-graph',
            figure = {
                'data':total,
                'layout': go.Layout(  
                        autosize=True,     
                        hovermode='closest',  
                        dragmode='select',     
                        title= '{0}宿舍{1}{2}对比'.format(self.sushe_id,subject,ScoreType[score_type]),
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
        
            
           

            

