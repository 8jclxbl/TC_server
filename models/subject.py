from app import db
from models.models import CurStudent,GradStudent,ControllerInfo,Controller,Consumption,Class_,Lesson,Teacher,Subject,StudyDays,Exam,ExamRes,ExamType
from models.student import get_all_subject,SUBJECTS
import pandas as pd


GENERE_SOCRE = [285,287,297,291,303,305]
NEED_PROCESS = [301,302,303]
CURRENT_THIRD = [i for i in range(916,926)]
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
        if not info: return None

    student_names = []
    student_ids = []

    for i in info:
        student_ids.append(i.id)
        student_names.append(i.name)

    data = {'student_id':student_ids,'student_name':student_names}
    return data

def get_exam_name():
    exams = db.session.query(Exam).all()
    exam_table = {}
    for i in exams:
        exam_table[i.id] = i.name.strip()
    return exam_table

EXAMS = get_exam_name()

def get_all_student_by_class_id(cla_id):
    return pd.DataFrame(get_all_student_by_class_id_raw(cla_id))

def get_all_grade_by_class_id(cla_id):
    students = get_all_student_by_class_id_raw(cla_id)
    if not students:return pd.DataFrame()

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
            subjects.append(SUBJECTS[j.subject_id] if j.subject_id > 0 else '缺失科目信息')
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
            exam_id.append(EXAMS[k])
            maxs.append(data.loc[max_[k]]['score'])
            mins.append(data.loc[min_[k]]['score'])

    res = {'subject':subjects_,'exam':exam_id,'max':maxs,'min':mins}
    return pd.DataFrame(res)

def get_7_3(cla_id):
    students = get_all_student_by_class_id_raw(cla_id)
    ids = students['student_id']
    names = students['student_name']
    length = len(ids)

    student_ids = []
    class_ids = []
    student_names = []
    subjects = []
 
    for i in range(length):
        student_ids.append(ids[i])
        student_names.append(names[i])
        class_ids.append(cla_id)

        sub_temp = set()
        for exam in NEED_PROCESS:
            info = db.session.query(ExamRes.subject_id,ExamRes.score).filter_by(exam_id = exam, student_id = ids[i]).all()
            sub_temp = sub_temp.union(set([i[0] for i in info if i[1] > 0]))
        if len(sub_temp) == 7:
            sub_temp = sub_temp.difference({1,2,3,59})
        else:
            sub_temp = sub_temp.difference({1,2,3})
        subjects.append([SUBJECTS[i] for i in sub_temp])

    data = {'student_id':student_ids,'student_name':student_names,'class_id':class_ids,'subject':subjects}
    return pd.DataFrame(data)

def get_7_3_by_df(df,cla_id):
    partition_by_exam = {}
    for exam in NEED_PROCESS:
        partition_by_exam[exam] = df.loc[(df['exam_id'] == exam) & (df['score']> 0)][['student_id','name','subject']]
    
    students = partition_by_exam[exam][['student_id','name']].drop_duplicates().values
 
    student_ids = []
    class_ids = []
    student_names = []
    subjects = []

    for i in students:
        student_ids.append(i[0])
        student_names.append(i[-1])
        class_ids.append(cla_id)
        sub_temp = set()
        for exam in NEED_PROCESS:
            cur = partition_by_exam[exam]
            subs = cur.loc[cur['student_id'] == i[0]]['subject'].values
            sub_temp = sub_temp.union(set(subs))
        if len(sub_temp) == 7:
            sub_temp = sub_temp.difference({'语文','数学','英语','技术'})
        elif len(sub_temp) == 6:
            sub_temp = sub_temp.difference({'语文','数学','英语'})
        if len(sub_temp) == 3:
            subjects.append(list(sub_temp))

    data = {'student_id':student_ids,'student_name':student_names,'class_id':class_ids,'subject':subjects}
    return pd.DataFrame(data)

def gen_all_table():
    temp = []
    for i in CURRENT_THIRD:
        temp.append(get_7_3(i))
        print(i)
    res = pd.concat(temp)
    res.to_csv('all_7_3.csv',encoding = 'utf-8')
    print('over')