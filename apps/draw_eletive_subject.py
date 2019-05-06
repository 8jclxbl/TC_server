import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go 
import pandas as pd

from dash.dependencies import Input,Output
from models.subject import sql_73,get_class_name
from app import app

PIE_COLOR_MAP = ['#b71c1c','#880E4F','#4A148C','#311B92','#1A237E','#0D47A1','#01579B','#006064','#004D40','#F57F17','#E65100',
                 '#BF360C','#ff1744','#F50057','#D500F9','#651FFF','#3D5AFE','#2979FF','#00B0FF','#00E5FF','#1DE9B6','#00E676',
                 '#FFEA00','#FF9100','#FF3D00','#ff5252', '#FF4081','#E040FB','#7C4DFF','#536DFE','#448AFF','#40C4FF','#18FFFF',
                 '#64FFDA','#69F0AE','#B2FF59','#EEFF41','#FFFF00','#FFD740','#FF6E40']

TRADITION_COLOR_MAP = ['#70f3ff','#44cef6','#3eede7','#1685a9','#177cb0','#065279','#003472','#4b5cc4','#2e4e7e','#3b2e7e','#8d4bbb','#003371','#56004f','#801dae','#ff461f','#ff2d51',
                       '#f36838','#ed5736','#ff4777','#f00056','#ffb3a7','#f47983','#db5a6b','#c93756','#f9906f','#f05654','#ff2121','#f20c00','#c83c23','#9d2933','#ff4c00','#ff4e20',
                       '#f35336','#dc3023','#ff3300','#cb3a56','#ef7a82','#ff0097','#c32136','#be002f','#c91f37', '#bf242a','#c3272b','#9d2933','#bce672','#c9dd22','#bddd22','#0eb83a',
                       '#0aa344','#16a951','#21a675','#057748','#0c8918','#00e500','#40de5a','#00e079','#00e09e','#3de1ad','#2add9c','#2edfa3','#7fecad','#a4e2c6','#7bcfa6','#1bd1a5']
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
                    plot_bgcolor="#191A1A",

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

    
    