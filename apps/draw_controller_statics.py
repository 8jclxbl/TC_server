import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go 
import pandas as pd

from dash.dependencies import Input,Output
from models.student import get_study_days_by_start_year
from app import app

type_class = {'arrive_late':[100000,100100,100200,100300,9900100,9900300],'leaving':[200200]}

def controller_statics_total(info,term,title):

    return dcc.Graph(
        id = 'controller-statics-pie',
        figure = {
            'data':[go.Pie(
                labels = ['出勤','迟到早退','请假'],
                values = info,
                
            )],
            'layout':go.Layout(
                title = title + '({0})'.format(term)
            )
        },
        style = {'margin-top':'10px'} 
    )

class controller_statics:
    def __init__(self,query_res):
        self.query_res = query_res
        self.type = 'pie'
        self.get_data()
        self.partition_term()
        self.term_p = self.partition_term()
        

    def get_data(self):
        self.data = self.query_res['data']
        self.type = self.query_res['type']
        self.id = self.query_res['id']
        self.terms = self.data['terms'].drop_duplicates().values
        self.types = self.data['types'].drop_duplicates().values
        self.title = '学生{0}考勤总体状况统计'.format(self.id)

    def gen_layout(self):
        layout = [
            html.Div(id = 'controller-static-container',children = [
                html.H6('请选择学期',style = {'display':'inline-block','margin-left':'10px','margin-left':'10px'}),
                html.Div(id = 'select-term', children = [
                    dcc.Dropdown(
                        id = 'term-selector',
                        options = [{'label':i,'value':i} for i in self.terms],
                        value = self.terms[0],
                        clearable = False
                    ),
                ],style = {'display':'inline-block','width':'30%','margin-left':'10px','margin-left':'10px','vertical-align':'middle'}),
            ]),
            
            html.Div(
                id = 'controller-statics',
            ),
        ]
        return layout
    
    def get_grade(self,cla_name):
        if '高一' in cla_name:
            return 1
        elif '高二' in cla_name:
            return 2
        elif '高三' in cla_name:
            return 3
        else:
            return 0

    def get_days(self,cla_name,term):
        st,en,ty = term.split('-') 
        info = get_study_days_by_start_year(st)
        grade = self.get_grade(cla_name)
        if ty == '1':
            if grade == 0:return 105
            else:return info[0]
        else:
            if grade == 0: return 93
            else:return info[grade]

    def partition_term(self):
        data = {}
        days_info = {}
        for i in self.terms:
            data[i] = self.data.loc[self.data['terms'] == i]
            cla_info = data[i].iloc[0]['class']
            days_info[i] = self.get_days(cla_info,i)

        self.p_term = data
        self.days = days_info

    def partition_type(self,term):
        if term not in self.p_term:
            return None
        else:
            temp = self.p_term[term]
            data = {}
            for i in self.types:
                data[i] = temp.loc[temp['types'] == i]
            return data

    def pie_data(self,term):
        cur_data = self.partition_type(term)
        arr_late = 0
        leaving = 0
        normal = self.days[term]
        for i in cur_data.keys():
            if i in type_class['arrive_late']:arr_late += len(cur_data[i].values)
            if i in type_class['leaving']:leaving += len(cur_data[i].values)
        normal = normal - arr_late - leaving
        return [normal,arr_late,leaving] 
        




