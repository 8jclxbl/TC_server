import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go 
import pandas as pd

from dash.dependencies import Input,Output
from models.subject import sql_73,get_class_name
from app import app

class EletiveSubject:
    def __init__(self, query_73):
        self.data = query_73
        self.subjects_process()

    def draw_pie(self,index,value):
        return dcc.Graph(
            id = 'suject-73-pie',
            figure = {
                'data':[go.Pie(
                    labels = index,
                    values = value,
                )],
                'layout':go.Layout(
                    title = '2018-2019学期高三七选三总体状况统计',
                    margin = {'t':100}
                )
            }
        )
    
    def draw_bar(self,index,value,id_,title_):
        return dcc.Graph(
            id = id_,
            figure = {
                'data':[go.Bar(
                    x = index,
                    y = value,
                )],
                'layout': go.Layout(  
                    hovermode='closest',  
                    dragmode='select',
                    plot_bgcolor="#191A1A",

                    title= title_,
                    xaxis = dict(title = '课程组合', showline = True, tickangle = 75),
                    yaxis = dict(title = '人数', showline = True),
                    margin=dict(l=40,r=40,b=140,t=80),
                )
            },
        )

    def draw_total(self):
        data = self.total_statics()
        index = data.index
        value = data.values
        return self.draw_pie(index,value)

    def draw_by_class(self,cla_id):
        data = self.statics_by_class(cla_id)
        index = data.index
        value = data.values
        return self.draw_bar(index,value,'class-bar-'+str(cla_id),get_class_name(cla_id) + '班七选三分布')

    def draw_by_one_subject(self):
        data = self.statics_by_one_subject()
        index = list(data.keys())
        value = list(data.values())
        return self.draw_bar(index,value,'one-subject-bar','单科选择分布')

    def draw_by_subjects(self,subjects):
        data = self.statics_by_subjects(subjects)
        index = data.index
        value = data.values
        return self.draw_bar(index,value,'subjects-bar',subjects)

    def subjects_process(self):
        temp = self.data['subjects'].values
        self.all_subject = []
        for i in range(len(temp)):
            cur = temp[i].split('|')
            self.all_subject += cur
            temp[i] = '|'.join(sorted(cur))
        self.data['subjects'] = temp
        self.combines = list(set(temp))

    def total_statics(self):
        return self.data.groupby('subjects').count()['student_id']

    def statics_by_subjects(self,subjects):
        data = self.data.loc[self.data['subjects'] == subjects]
        return data.groupby('class_id').count()['student_id']

    def statics_by_class(self,class_id):
        data = self.data.loc[self.data['class_id'] == class_id]
        return data.groupby('subjects').count()['student_id']

    def statics_by_one_subject(self):
        counter = {}
        for i in self.all_subject:
            if i not in counter:
                counter[i] = 1
            else:
                counter[i] += 1
        return counter

    
    