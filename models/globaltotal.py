from app import db,session
from models.models import CurStudent,GradStudent,ControllerInfo,Controller,Consumption,Class_,Lesson,Teacher,Subject,StudyDays,Exam,ExamRes,ExamType
import pandas as pd

#获取全部的科目信息
def get_all_subject():
    subjects = db.session.query(Subject).all()
    sub_dic = {}
    for i in subjects:
        sub_dic[i.id] = i.name
    sub_dic[-1] = '此次考试科目数据缺失'
    return sub_dic

def get_all_controller():
    controllers = db.session.query(Controller).all()
    controllers_table = {}
    for i in controllers:
        controllers_table[i.task_id] = i.name + ':' + i.task_name
    return controllers_table

#获取所有的考试名称
def get_exam_name():
    exams = db.session.query(Exam).all()
    exam_table = {}
    for i in exams:
        exam_table[i.id] = i.name.strip()
    return exam_table

#获取所有的有班级的学期
def get_terms_of_all_class():
    info = session.query(Class_.term).all()
    data = [i[0] for i in info]
    return sorted(list(set(data)))

def get_all_grades():
    total_grades = pd.read_csv('./static/examres.csv')
    return total_grades

SUBJECTS = get_all_subject()
#EXAMS = get_all_exam_type()
GRADETYPE = {-2:'缺考',-1:'作弊',-3:'免考',-6:'缺失数据'}

CONTROLLER_TABLE = get_all_controller()

#需要处理的三次考试，用于计算7选三
NEED_PROCESS = [301,302,303]
#当前高三的id
CURRENT_THIRD = [i for i in range(916,926)]
#七选三的备选课程
ELETIVE_CLASS = ['政治','历史','地理','物理','化学','生物','技术']

CLASS_TERMS = get_terms_of_all_class()

EXAMS = get_exam_name()

GENERE_EXAM_ID = [285,287,291,297,303,305]

TOTAL_GRADE = get_all_grades()

THIRD_GRADE = {916: '高三(02)',917: '高三(03)',918: '高三(04)',919: '高三(07)',920: '高三(08)',
               921: '高三(01)',922: '高三(05)',923: '高三(09)',924: '高三(06)',925: '高三(10)'}

SUBJECT_COLOR = {'语文':'#b71c1c','数学':'#0D47A1','英语':'#FFEB3B','物理':'#4A148C','化学':'#AB47BC',
                 '生物':'#880E4F','历史':'#ef5350','地理':'#F06292','体育':'#1B5E20','音乐':'#4CAF50',
                 '美术':'#009688','信息技术':'#006064','政治':'#FF6F00','科学':'#00796B','通用技术':'#26C6DA',
                 '英语选修9':'#F9A825','1B模块总分':'#4E342E','英语2':'#FFF59D','技术':'#00838F','此次考试科目数据缺失':'#212121'}
SOCRE_TYPE_COLOR = {'score':'#303952','z_score':'#596275','t_score':'#786fa6','r_score':'#574b90'}


PIE_COLOR_MAP = ['#b71c1c','#880E4F','#4A148C','#311B92','#1A237E','#0D47A1','#01579B','#006064','#004D40','#F57F17','#E65100',
                 '#BF360C','#ff1744','#F50057','#D500F9','#651FFF','#3D5AFE','#2979FF','#00B0FF','#00E5FF','#1DE9B6','#00E676',
                 '#FFEA00','#FF9100','#FF3D00','#ff5252', '#FF4081','#E040FB','#7C4DFF','#536DFE','#448AFF','#40C4FF','#18FFFF',
                 '#64FFDA','#69F0AE','#B2FF59','#EEFF41','#FFFF00','#FFD740','#FF6E40']

TRADITION_COLOR_MAP = ['#70f3ff','#44cef6','#3eede7','#1685a9','#177cb0','#065279','#003472','#4b5cc4','#2e4e7e','#3b2e7e','#8d4bbb','#003371','#56004f','#801dae','#ff461f','#ff2d51',
                       '#f36838','#ed5736','#ff4777','#f00056','#ffb3a7','#f47983','#db5a6b','#c93756','#f9906f','#f05654','#ff2121','#f20c00','#c83c23','#9d2933','#ff4c00','#ff4e20',
                       '#f35336','#dc3023','#ff3300','#cb3a56','#ef7a82','#ff0097','#c32136','#be002f','#c91f37', '#bf242a','#c3272b','#9d2933','#bce672','#c9dd22','#bddd22','#0eb83a',
                       '#0aa344','#16a951','#21a675','#057748','#0c8918','#00e500','#40de5a','#00e079','#00e09e','#3de1ad','#2add9c','#2edfa3','#7fecad','#a4e2c6','#7bcfa6','#1bd1a5']

CONTROLLER_COLOR = {100000:'#1A237E',100100:'#303F9F',100200:'#3F51B5',100300:'#7986CB',
                    200000:'#4A148C',200100:'#7B1FA2',200200:'#9C27B0',
                    300000:'#b71c1c',300100:'#d32f2f',300200:'#f44336',
                    9900100:'#1B5E20',9900200:'#388E3C',9900300:'#4CAF50',9900400:'#558B2F',9900500:'#7CB342'}