from app import session
from models.models import CurStudent,GradStudent,ControllerInfo,Controller,Consumption,Class_,Lesson,Teacher,Subject,StudyDays,Exam,ExamRes,ExamType,SubjectSelect
from models.globaltotal import SUBJECTS,NEED_PROCESS,CURRENT_THIRD,ELETIVE_CLASS,CLASS_TERMS,EXAMS,TOTAL_GRADE,ALL_CLASSES
import pandas as pd

"""
#获取所有的班级，返回字典结构
def get_all_calsses_raw():
    info = session.query(Class_).all()

    class_ids = []
    class_terms = []
    class_names = []

    for i in info:
        if 'IB' in i.name:continue
        class_ids.append(i.id)
        class_terms.append(i.term)
        class_names.append(i.name)

    return {'id':class_ids,'term':class_terms,'name':class_names}
    
#获取所有的班级，返回df
def get_all_calsses():
    data = get_all_calsses_raw()
    return pd.DataFrame(data)

def get_classes_by_term(term):
    info = session.query(Class_).filter_by(term = term).all()
    
    class_ids = []
    class_terms = []
    class_names = []

    for i in info:
        if 'IB' in i.name:continue
        class_ids.append(i.id)
        class_terms.append(term)
        class_names.append(i.name)
    data = {'id':class_ids,'term':class_terms,'name':class_names}
    return pd.DataFrame(data)
"""


def get_classes_by_term(term):
    info = ALL_CLASSES.loc[ALL_CLASSES['class_term'] == term]

    class_ids = []
    class_terms = []
    class_names = []

    for i in info.values:
        if 'IB' in i[2]:continue
        class_ids.append(i[0])
        class_terms.append(i[1])
        class_names.append(i[2])
    data = {'id':class_ids,'term':class_terms,'name':class_names}

    return pd.DataFrame(data)

#根据班级id获取所有的学生，返回字典结构
def get_all_student_by_class_id_raw(cla_id):
    cla_id = int(cla_id)
    info = session.query(CurStudent.id,CurStudent.name).filter_by(class_id = cla_id).all()
    if not info:
        info = session.query(GradStudent).filter_by(class_id = cla_id).all()
        if not info: return None

    student_names = []
    student_ids = []

    for i in info:
        student_ids.append(i.id)
        student_names.append(i.name)

    data = {'student_id':student_ids,'student_name':student_names}
    return data

#根据班级id
def get_all_student_by_class_id(cla_id):
    return pd.DataFrame(get_all_student_by_class_id_raw(cla_id))


#根据班级id获取班级学生和姓名的对照字典
def get_all_dict_by_class_id(cla_id):
    cla_id = int(cla_id)
    info = session.query(CurStudent.id,CurStudent.name).filter_by(class_id = cla_id).all()
    if not info:
        info = session.query(GradStudent).filter_by(class_id = cla_id).all()
        if not info: return None
    student = {}
    for i in info:
        student[i.id] = i.name
    return student

#已经CSV化
#根据班级id获取所有的总分
def get_all_grade_by_class_id_total(cla_id):
    cla_id = int(cla_id)
    data = TOTAL_GRADE.loc[TOTAL_GRADE['class_id'] == cla_id].copy()
    subjects = [SUBJECTS[i] for i in data.subject_id.values]
    data['subject'] = subjects

    return data[['student_id','exam_id','subject','score','z_score','t_score','r_score','div']]

#获取一个班级所有考试的最高分和最低分
def class_grade_process(df):
    #考试的学科
    subjects = df['subject'].drop_duplicates().values

    subjects_ = []
    exam_id = []
    exam_name = []
    maxs = []
    mins = []

    for i in subjects:
        data = df.loc[(df['subject'] == i) & (df['score'] > 0)]
        group_by_exam = data.groupby('exam_id')
        max_ = group_by_exam['score'].idxmax()
        min_ = group_by_exam['score'].idxmin()

        for k in max_.keys():
            subjects_.append(i)
            exam_id.append(k)
            exam_name.append(EXAMS[k])
            maxs.append(data.loc[max_[k]]['score'])
            mins.append(data.loc[min_[k]]['score'])

    res = {'subject':subjects_,'exam':exam_name,'exam_id':exam_id,'max':maxs,'min':mins}
    return pd.DataFrame(res)

#基于之前获取的7选三表，直接读取七选三数据
def sql_73(cla_id = None):
    if not cla_id:
        info = session.query(SubjectSelect).all()
    else:
        info = session.query(SubjectSelect).filter_by(class_id = cla_id).all()
    student_ids = []
    student_names = []
    class_ids = []
    subject_names = []
    for i in info:
        student_ids.append(i.student_id)
        student_names.append(i.student_name)
        class_ids.append(i.class_id)
        subject_names.append(i.subjects)

    data = {'student_id':student_ids,'student_name':student_names,'class_id':class_ids,'subjects':subject_names}
    return pd.DataFrame(data)
