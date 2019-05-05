from app import db
from models.models import CurStudent,GradStudent,ControllerInfo,Controller,Consumption,Class_,Lesson,Teacher,Subject,StudyDays,Exam,ExamRes,ExamType,SubjectSelect
from models.student import get_all_subject,SUBJECTS
import pandas as pd

#平时成绩的考试id
GENERE_SOCRE = [285,287,297,291,303,305]
#需要处理的三次考试，用于计算7选三
NEED_PROCESS = [301,302,303]
#当前高三的id
CURRENT_THIRD = [i for i in range(916,926)]
#七选三的备选课程
ELETIVE_CLASS = ['政治','历史','地理','物理','化学','生物','技术']

#获取所有的班级，返回字典结构
def get_all_calsses_raw():
    info = db.session.query(Class_).all()

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

def get_class_name(cla_id):
    info = db.session.query(Class_.name).filter_by(id = cla_id).first()
    return info[0]

def get_classes_by_term(term):
    info = db.session.query(Class_).filter_by(term = term).all()
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

#获取所有的有班级的学期
def get_terms_of_all_class():
    data = get_all_calsses_raw()
    return sorted(list(set(data['term'])))


CLASS_TERMS = get_terms_of_all_class()

#根据班级id获取所有的学生，返回字典结构
def get_all_student_by_class_id_raw(cla_id):
    cla_id = int(cla_id)
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

#获取所有的考试名称
def get_exam_name():
    exams = db.session.query(Exam).all()
    exam_table = {}
    for i in exams:
        exam_table[i.id] = i.name.strip()
    return exam_table

EXAMS = get_exam_name()

#根据班级id
def get_all_student_by_class_id(cla_id):
    return pd.DataFrame(get_all_student_by_class_id_raw(cla_id))

#根据班级id获取班级学生和姓名的对照字典
def get_all_dict_by_class_id(cla_id):
    cla_id = int(cla_id)
    info = db.session.query(CurStudent.id,CurStudent.name).filter_by(class_id = cla_id).all()
    if not info:
        info = db.session.query(GradStudent).filter_by(class_id = cla_id).all()
        if not info: return None

    student = {}

    for i in info:
        student[i.id] = i.name

    return student

#根据班级id获取班级成绩
def get_all_grade_by_class_id(cla_id):
    students = get_all_dict_by_class_id(cla_id)
    info = db.session.query(ExamRes).filter_by(class_id = cla_id).all()

    exam_ids = []
    student_names = []
    subjects = []
    scores = []
    z_scores = []
    t_scores = []
    r_scores = []
    student_ids = []
     
    for i in info:
        student_ids.append(i.student_id)
        student_names.append(students[i.student_id])
        exam_ids.append(i.exam_id)
        subjects.append(SUBJECTS[i.subject_id] if i.subject_id > 0 else '缺失科目信息')
        scores.append(i.score)
        z_scores.append(i.z_score)
        t_scores.append(i.t_score)
        r_scores.append(i.r_score)

    data = {'student_id':student_ids,'name':student_names,'exam_id':exam_ids,'subject':subjects,
            'score':scores,'z_score':z_scores,'t_score':t_scores,'r_score':r_scores}
    return pd.DataFrame(data)

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
            exam_id.append(EXAMS[k])
            maxs.append(data.loc[max_[k]]['score'])
            mins.append(data.loc[min_[k]]['score'])

    res = {'subject':subjects_,'exam':exam_id,'max':maxs,'min':mins}
    return pd.DataFrame(res)

#基于之前获取的7选三表，直接读取七选三数据
def sql_73(cla_id = None):
    if not cla_id:
        info = db.session.query(SubjectSelect).all()
    else:
        info = db.session.query(SubjectSelect).filter_by(class_id = cla_id).all()
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

#计算七选三数据
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

#计算七选三数据，较上面的函数快一些
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
