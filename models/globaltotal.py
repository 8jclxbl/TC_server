import pandas as pd

#pure_scv,去除数据库，直接将数据读入内存

STATIC_PATH = './static/'
FILE_NAME = {
    'classes':'class_.csv',                                                        #班级信息
    'subjects':'subject.csv',                                                     #学科信息             
    'controller_type':'controller.csv',                                      #考勤类型
    'controller_infos':'controller_info.csv',                             #考勤信息
    'exams':'exam.csv',                                                             #考试信息
    'exam_results':'examres.csv',                                              #考试成绩
    'total_grade_and_rank':'total_gc_rank.csv',                        #考试总分 
    'dorms':'sushe.csv',                                                               #宿舍信息
    'current_student':'cur_student.csv',                                       #在校学生
    'graduated_student':'grad_student.csv',                                 #毕业学生
    'lessons':'lesson.csv',                                                             #课程信息
    'study_days':'study_days.csv',                                              #在校天数
    'consumptions':'consumption.csv',                                       #消费信息
    'consumption_predicts':'consumption_predict.csv',            #消费预测
    'rank_predicts':'rank_predict.csv',                                       #等地预测
    'subjects_select':'process_7_3.csv'                                      #七选三信息
}


def get_csv_data(fileName):
    file_path = STATIC_PATH + FILE_NAME[fileName]
    data = pd.read_csv(file_path)
    return data

#获取全部的班级信息
def get_all_class():
    classes = get_csv_data('classes')
    return classes

#获取全部的科目信息
def get_all_subject():
    subjects = get_csv_data('subjects')
    ids = subjects['id'].values
    names = subjects['name'].values
    sub_dic = {k:v for k,v in zip(ids,names)}
    sub_dic[-1] = '此次考试科目数据缺失'
    return sub_dic

def get_all_controller():
    controller_type = get_csv_data('controller_type')
    ids = controller_type['task_id'].values
    names = controller_type['name'].values
    task_names = controller_type['task_name'].values
    total_names = [i+';'+j for i,j in zip(names,task_names)]
    controllers_dic = {k:v for k,v in zip(ids, total_names)}
    return controllers_dic

def get_all_controller_info():
    controller_infos = get_csv_data('controller_infos')
    return controller_infos

#获取所有的考试名称
def get_exam_name():
    exams = get_csv_data('exams')
    ids = exams['id'].values
    names = exams['name'].values
    exam_dic = {k:v.strip() for k,v in zip(ids,names)}
    return exam_dic

#获取所有的有班级的学期
def get_terms_of_all_class(all_classes):
    terms = all_classes.class_term
    terms_dd = terms.drop_duplicates().values
    #terms_dd = [i for i in terms_dd if i[-1] != '2']
    terms_sorted = sorted(terms_dd)
    return terms_sorted

def get_all_grades():
    exam_results = get_csv_data('exam_results')
    return exam_results

#获取所有的总分
def get_all_totals():
    total_grade_and_rank = get_csv_data('total_grade_and_rank')
    return total_grade_and_rank

def get_all_dorms():
    dorms = get_csv_data('dorms')
    return dorms

def get_class_has_dorm(dorms_info):
    info = dorms_info.class_id.drop_duplicates().values
    return sorted(info)

def get_class_table(all_classes):
    ids = all_classes.class_id.values
    names = all_classes.class_name.values
    return {k:v for k,v in zip(ids,names)}

def get_cur_student():
    current_student = get_csv_data('current_student')
    return current_student

def get_grad_student():
    graduated_student = get_csv_data('graduated_student')
    return graduated_student

def get_all_lesson():
    lessons = get_csv_data('lessons')
    return lessons

def get_study_day():
    study_days = get_csv_data('study_days')
    return study_days

def get_all_consumption():
    consumptions = get_csv_data('consumptions')
    return consumptions

def get_all_consumption_predict():
    consumption_predicts = get_csv_data('consumption_predicts')
    return consumption_predicts

def get_all_rank_predict():
    rank_predicts = get_csv_data('rank_predicts')
    return rank_predicts

def get_all_subject_73():
    subjects_select = get_csv_data('subjects_select')
    return subjects_select

ALL_CLASSES = get_all_class()
SUBJECTS = get_all_subject()
#EXAMS = get_all_exam_type()
GRADETYPE = {-2:'缺考',-1:'作弊',-3:'免考',-6:'缺考,作弊,免考'}

CONTROLLER_TABLE = get_all_controller()

CUR_STUDENT = get_cur_student()
GRAD_STUDENT = get_grad_student()
CONTROLLER_INFO = get_all_controller_info()
STUDYDAYS = get_study_day()
CONSUMPTION = get_all_consumption()
CONSUMPTION_PREDICT = get_all_consumption_predict()
RANK_PREDICT = get_all_rank_predict()
ALL_SUBJECT_73 = get_all_subject_73()

LESSON = get_all_lesson()
#需要处理的三次考试，用于计算7选三
NEED_PROCESS = [301,302,303]
#当前高三的id
CURRENT_THIRD = [i for i in range(916,926)]
#七选三的备选课程
ELETIVE_CLASS = ['政治','历史','地理','物理','化学','生物','技术']
CLASS_TERMS = get_terms_of_all_class(ALL_CLASSES)
CLASS_TABLE = get_class_table(ALL_CLASSES)
EXAMS = get_exam_name()
GENERE_EXAM_ID = [285,287,291,297,303,305]
TOTAL_GRADE = get_all_grades()
TOTAL_TOTALS = get_all_totals()
DORMS_INFO = get_all_dorms()
CLASS_HAS_DORM = get_class_has_dorm(DORMS_INFO)

THIRD_GRADE = {916: '高三(02)',917: '高三(03)',918: '高三(04)',919: '高三(07)',920: '高三(08)',
               921: '高三(01)',922: '高三(05)',923: '高三(09)',924: '高三(06)',925: '高三(10)'}


#色表
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

CONTROLLER_COLOR = {100000:'#4db6ac',100100:'#004d40',100200:'#64ffda',100300:'#006064',
                    200000:'#ff7043',200100:'#bf360c',200200:'#dd2c00',
                    300000:'#ffd600',300100:'#fff176',300200:'#eeff41',
                    9900100:'#d50000',9900200:'#ff8a80',9900300:'#e57373',9900400:'#c51162',9900500:'#ec407a'}