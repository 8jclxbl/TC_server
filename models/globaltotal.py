import pandas as pd
#pure_scv,去除数据库，直接将数据读入内存
#此文件集成了服务所需要的所有数据的获取

STATIC_PATH = './static/'

#对应的文件名称
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

#使用pd.read_csv读取csv文件
#Input: fileName 文件名 'str',
#return: data 对应的数据 'pd.DataFrame
def get_csv_data(fileName):
    file_path = STATIC_PATH + FILE_NAME[fileName]
    data = pd.read_csv(file_path)
    return data

#获取全部的班级信息
#return: classes 班级信息 'pd.DataFrame
#classes.columns = [class_id,class_term,class_name,grade_name]
def get_all_class():
    classes = get_csv_data('classes')
    return classes

#获取全部的科目信息
#return: sub_dic 科目信息的字典 'dict'
#sub_dic: keys, 科目id; values, 科目名称
#   额外加入了-1，用于表示缺失的科目
def get_all_subject():
    subjects = get_csv_data('subjects')
    ids = subjects['id'].values
    names = subjects['name'].values
    sub_dic = {k:v for k,v in zip(ids,names)}
    sub_dic[-1] = '此次考试科目数据缺失'
    return sub_dic

#获取所有的考勤类型
#return: controllers_dic  'dict'
#controllers_dic: keys 考勤类型的id; values 考勤类型的名称
def get_all_controller():
    controller_type = get_csv_data('controller_type')
    ids = controller_type['task_id'].values
    names = controller_type['name'].values
    task_names = controller_type['task_name'].values
    total_names = [i+';'+j for i,j in zip(names,task_names)]
    controllers_dic = {k:v for k,v in zip(ids, total_names)}
    return controllers_dic

#获取所有的考勤信息
#return: controller_infos 'pd.DataFrame'
#controller_infos.columns = [id,term,date_time,type_id,class_id,student_id,class_name]
def get_all_controller_info():
    controller_infos = get_csv_data('controller_infos')
    return controller_infos

#获取所有的考试名称
#return: exam_dic 'dict'
#exam_dic: keys 考试的id; values 考试的名称
def get_exam_name():
    exams = get_csv_data('exams')
    ids = exams['id'].values
    names = exams['name'].values
    exam_dic = {k:v for k,v in zip(ids,names)}
    return exam_dic

#获取所有的有班级的学期
#return:term_results  有班级信息的学期 'list'
def get_terms_of_all_class(all_classes):
    terms = all_classes.class_term
    terms_dd = terms.drop_duplicates().values
    terms_sorted = sorted(terms_dd)
    return terms_sorted

def get_class_year_of_all_class(all_classes):
    years = all_classes['class_year']
    years_d = years.drop_duplicates().values
    years_sorted = sorted(years_d)
    return years_sorted

#获取所有的考试信息，经过处理后的考试信息，加入了考试离均值，班级排名和年级排名
#return: exam_results 'pd.DataFrame'
#exam_results.columns = [test_id,exam_id,subject_id,student_id,class_id,grade,score,z_score,t_score,r_score,mean,div,rank,class_rank]
def get_all_grades():
    exam_results = get_csv_data('exam_results')
    return exam_results

#获取所有的总分信息，是将上面的考试成绩，基于每次考试的每个学生求得总分，班级排名和年级排名
#return: total_grade_and_rank 'pd.DataFrame'
#total_grade_and_rank.columns = [stu_id,exam,total,grade,class,rank,mean,div,class_rank]
def get_all_totals():
    total_grade_and_rank = get_csv_data('total_grade_and_rank')
    return total_grade_and_rank

#获取所有的宿舍信息，基于学生信息表，获取住校学生的信息
#return: dorms 'pd.DataFrame'
#dorms.columns = ['student_id,student_name,student_sex,class_id,sushe_id]
def get_all_dorms():
    dorms = get_csv_data('dorms')
    return dorms

#基于整体的宿舍信息，获取有住校学生的班级的id的列表
#Input: dorms_info, 'pd.DataFrame'
#return: info 'list'
def get_class_has_dorm(dorms_info):
    info = dorms_info.class_id.drop_duplicates().values
    return sorted(info)

#基于所有的班级信息，获取班级id和班级名称的字典
#Input: all_classes, 'pd.DataFrame'
#return: 'dict'
#keys 班级id; values 班级名称
def get_class_table(all_classes):
    ids = all_classes.class_id.values
    names = all_classes.class_name.values
    return {k:v for k,v in zip(ids,names)}

#基于初始的学生信息表生成的在校学生数据
#return: current_student 'pd.DataFrame'
#current_student.columns = [id,name,sex,nation,born_year,native,residence,class_id,class_name,class_term,policy,zhusu,leave_school,qinshihao]
def get_cur_student():
    current_student = get_csv_data('current_student')
    return current_student

#基于考勤和消费信息获取的不在上面的在校学生数据的学生数据，由于此表中的学生数据只有部分特征，所以分成两个表
#return: graduated_student 'pd.DataFrame'
#graduated_student.columns = [id,name,class_id,class_name,class_term]
def get_grad_student():
    graduated_student = get_csv_data('graduated_student')
    return graduated_student

#获取所有的课程信息，在设计数据库的时候，把课程和教师的数据划分了，这个表的划分继承了数据库中的设计
#return: lessons 'pd.DataFrame'
#lessons.columns = [subject_id,class_id,teacher_id,teacher_name]
def get_all_lesson():
    lessons = get_csv_data('lessons')
    return lessons

#基于效实中学的官网给出的校历，计算出的各个学期的在校天数
#return: study_days
#study_days.columns = [year,term_one,term_two_first,term_two_second,term_three_third]
def get_study_day():
    study_days = get_csv_data('study_days')
    return study_days

#获取所有的消费信息
#return: consumptions 'pd.DataFrame'
#consumptions.columns = [date_time,money,student_id,date,time]
def get_all_consumption():
    consumptions = get_csv_data('consumptions')
    return consumptions

#获取我们预测的下个月的消费
#return: consumption_predicts 'pd.DataFrame'
#consumption_predicts.columns = [student_id,money,consumption_mode]
def get_all_consumption_predict():
    consumption_predicts = get_csv_data('consumption_predicts')
    return consumption_predicts

#获取我们预测的下次考试的等第
#return: rank_predicts 'pd.DataFrame'
#rank_predicts.columns = [student_id,subject_id,r_score]
def get_all_rank_predict():
    rank_predicts = get_csv_data('rank_predicts')
    return rank_predicts

#获取处理后所得的所有的7选三数据，原本设计的是在线生成，后来出于响应速度的考虑采用预先计算的结果
#return subjects_select 'pd.columns'
#subjects_select = [student_id,student_name,class_id,subjects]
def get_all_subject_73():
    subjects_select = get_csv_data('subjects_select')
    return subjects_select

ALL_CLASSES = get_all_class()
SUBJECTS = get_all_subject()
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
CLASS_YEARS = get_class_year_of_all_class(ALL_CLASSES)
CLASS_TABLE = get_class_table(ALL_CLASSES)
EXAMS = get_exam_name()

#平时成绩的考试ID
GENERE_EXAM_ID = [285,287,291,297,303,305]
TOTAL_GRADE = get_all_grades()
TOTAL_TOTALS = get_all_totals()
DORMS_INFO = get_all_dorms()
CLASS_HAS_DORM = get_class_has_dorm(DORMS_INFO)

#当前高三的表
THIRD_GRADE = {916: '高三(02)',917: '高三(03)',918: '高三(04)',919: '高三(07)',920: '高三(08)',
               921: '高三(01)',922: '高三(05)',923: '高三(09)',924: '高三(06)',925: '高三(10)'}

#色表
SUBJECT_COLOR = {'语文':'#b71c1c','数学':'#0D47A1','英语':'#FFEB3B','物理':'#4A148C','化学':'#AB47BC',
                 '生物':'#880E4F','历史':'#ef5350','地理':'#F06292','体育':'#1B5E20','音乐':'#4CAF50',
                 '美术':'#009688','信息技术':'#006064','政治':'#FF6F00','科学':'#00796B','通用技术':'#26C6DA',
                 '英语选修9':'#F9A825','1B模块总分':'#4E342E','英语2':'#FFF59D','技术':'#00838F','此次考试科目数据缺失':'#212121'}
SOCRE_TYPE_COLOR = {'score':'#303952','z_score':'#596275','t_score':'#786fa6','r_score':'#574b90'}


PIE_COLOR_MAP =['#aa2d79','#d72a77','#da2c69','#d92c57','#d72f3e','#d9302c','#de5024','#dc6326',
                 '#e37f33','#ef941b','#efdb1b','#f3e731','#bdd032','#abce34','#70b443','#2aa252',
                 '#28a444','#069545','#049453','#01966c','#00958f','#0196b4','#03a2db','#2899d8',
                 '#2390c7','#2079b5','#1b619f','#1f488a','#20378a','#342675','#492579','#5f2975',
                 '#7c2c82','#812d78','#ad2b97']

TRADITION_COLOR_MAP = ['#70f3ff','#44cef6','#3eede7','#1685a9','#177cb0','#065279','#003472','#4b5cc4','#2e4e7e','#3b2e7e','#8d4bbb','#003371','#56004f','#801dae','#ff461f','#ff2d51',
                       '#f36838','#ed5736','#ff4777','#f00056','#ffb3a7','#f47983','#db5a6b','#c93756','#f9906f','#f05654','#ff2121','#f20c00','#c83c23','#9d2933','#ff4c00','#ff4e20',
                       '#f35336','#dc3023','#ff3300','#cb3a56','#ef7a82','#ff0097','#c32136','#be002f','#c91f37', '#bf242a','#c3272b','#9d2933','#bce672','#c9dd22','#bddd22','#0eb83a',
                       '#0aa344','#16a951','#21a675','#057748','#0c8918','#00e500','#40de5a','#00e079','#00e09e','#3de1ad','#2add9c','#2edfa3','#7fecad','#a4e2c6','#7bcfa6','#1bd1a5']

CONTROLLER_COLOR = {100000:'#4db6ac',100100:'#004d40',100200:'#64ffda',100300:'#006064',
                    200000:'#ff7043',200100:'#bf360c',200200:'#dd2c00',
                    300000:'#ffd600',300100:'#fff176',300200:'#eeff41',
                    9900100:'#d50000',9900200:'#ff8a80',9900300:'#e57373',9900400:'#c51162',9900500:'#ec407a'}