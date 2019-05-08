import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go 
import pandas as pd

from dash.dependencies import Input,Output
from models.subject import get_class_name
from models.globaltotal import PIE_COLOR_MAP
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
                    marker = dict(colors = PIE_COLOR_MAP[:len(index)]),
                )],
                'layout':go.Layout(
                    title = {'text':'2018-2019学期高三七选三总体状况统计','y':0.95},
                    margin = {'t':100},
                )
            }
        )
    
    def draw_bar(self,index,value,x_title,y_title,id_,title_):
        return dcc.Graph(
            id = id_,
            figure = {
                'data':[go.Bar(
                    x = index,
                    y = value,
                    width = [0.4] * len(index)
                )],
                'layout': go.Layout(  
                    hovermode='closest',  
                    dragmode='select',
                    plot_bgcolor="#dfe6e9",

                    title= title_,
                    xaxis = dict(title = x_title, showline = True, tickangle = 75),
                    yaxis = dict(title = y_title, showline = True),
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
        return self.draw_bar(index,value,'class-bar-'+str(cla_id),'课程组合','人数',get_class_name(cla_id) + '班七选三分布')

    def draw_by_one_subject(self):
        data = self.statics_by_one_subject()
        index = list(data.keys())
        value = list(data.values())
        return self.draw_bar(index,value,'课程','人数','one-subject-bar','单科选择分布')

    def draw_by_subjects(self,subjects):
        data = self.statics_by_subjects(subjects)
        index = data.index
        index = [get_class_name(i) + '班' for i in index]
        value = data.values
        return self.draw_bar(index,value,'班级','人数','subjects-bar',subjects)

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

    
    