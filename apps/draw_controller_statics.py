import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go 

from app import app

TYPE_CLASS = {'arrive_late':[100000,100100,100200,100300,9900100,9900300],'leaving':[200200]}

def controller_sta_table

def gen_terms_list(st_year = 13,en_year = 18,st_type = 1, end_type = 1):
    term_type = st_type
    cur_year = st_year

    res = []
    f = lambda s,e,t:'20{0}-20{1}-{2}'.format(s,e,t)
    while cur_year < en_year:
        res.append(f(cur_year,cur_year+1,term_type))
        if term_type == 1:
            term_type = 2
        else:
            term_type = 1
            cur_year += 1

    res.append(f(en_year,en_year+1,1))
    if end_type == 2:
        res.append(f(en_year,en_year+1,2))
    return res

