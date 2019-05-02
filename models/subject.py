from app import db
from models.models import CurStudent,GradStudent,ControllerInfo,Controller,Consumption,Class_,Lesson,Teacher,Subject,StudyDays,Exam,ExamRes,ExamType
from models.student import get_all_subject,SUBJECTS
import pandas as pd


GENERE_SOCRE = [285,287,297,291,303,305]
def get_all_calsses_raw():
    info = db.session.query(Class_).all()

    class_ids = []
    class_terms = []
    class_names = []

    for i in info:
        class_ids.append(i.id)
        class_terms.append(i.term)
        class_names.append(i.name)

    return {'id':class_ids,'term':class_terms,'name':class_names}
    
def get_all_calsses():
    data = get_all_calsses_raw()
    return pd.DataFrame(data)

def get_terms_of_all_class():
    info = db.session.query(Class_.term).group_by(Class_.term).all()
    info = [str(i[0]) for i in info]
    return info

def get_all_student_by_class_id_raw(cla_id):
    info = db.session.query(CurStudent.id,CurStudent.name).filter_by(class_id = cla_id).all()
    if not info:
        info = db.session.query(GradStudent).filter_by(class_id = cla_id).all()
        if not info: return {'id':'cla_id','data':None}

    student_names = []
    student_ids = []

    for i in info:
        student_ids.append(i.id)
        student_names.append(i.name)

    data = {'student_id':student_ids,'student_name':student_names}
    return data

def get_all_student_by_class_id(cla_id):
    return pd.DataFrame(get_all_student_by_class_id_raw(cla_id))

def get_all_grade_by_class_id(cla_id):
    students = get_all_student_by_class_id_raw(cla_id)

    exam_ids = []
    student_names = []
    subjects = []
    scores = []
    z_scores = []
    t_scores = []
    r_scores = []
    student_ids = []
     
    ids = students['student_id']
    names = students['student_name']
    student_num = len(ids)
    

    for i in range(student_num):
        cur_info = db.session.query(ExamRes).filter_by(student_id = ids[i]).all()
        for j in cur_info:
            student_ids.append(ids[i])
            student_names.append(names[i])
            exam_ids.append(j.exam_id)
            subjects.append(SUBJECTS[j.subject_id])
            scores.append(j.score)
            z_scores.append(j.z_score)
            t_scores.append(j.t_score)
            r_scores.append(j.r_score)

    data = {'student_id':student_ids,'name':student_names,'exam_id':exam_ids,'subject':subjects,
            'score':scores,'z_score':z_scores,'t_score':t_scores,'r_score':r_scores}
    return pd.DataFrame(data)

CLASS_TERMS = get_terms_of_all_class()

def class_grade_process(df):
    subjects = df['subject'].drop_duplicates().values

    subjects_ = []
    exam_id = []
    maxs = []
    mins = []

    for i in subjects:
        data = df.loc[df['subject'] == i]
        group_by_exam = data.groupby('exam_id')
        max_ = group_by_exam['score'].idxmax()
        min_ = group_by_exam['score'].idxmin()

        for k in max_.keys():
            subjects_.append(i)
            exam_id.append(k)
            maxs.append(data.loc[max_[k]]['score'])
            mins.append(data.loc[min_[k]]['score'])

    res = {'subject':subjects_,'exam':exam_id,'max':maxs,'min':mins}
    return pd.DataFrame(res)