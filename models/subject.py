from models.globaltotal import SUBJECTS,EXAMS,TOTAL_GRADE,ALL_CLASSES,CUR_STUDENT,GRAD_STUDENT,ALL_SUBJECT_73,LESSON
import pandas as pd

#根据学期获取当前学期的班级数据
#input: term 'str'
#return: 'pd.dataFrame'
#{'id','term','name','grade_name'}
def get_classes_by_term(term):
    info = ALL_CLASSES.loc[ALL_CLASSES['class_term'] == term]
    mask = []
    for i in info['class_name'].values:
        if 'IB' in i:mask.append(False)
        else:mask.append(True)
    
    without_ib = info.iloc[mask][['class_id', 'class_term', 'class_name', 'grade_name']]
    without_ib.columns = ['id','term','name','grade_name']
    return without_ib

def get_classes_by_term_dic(term):
    df = get_classes_by_term(term)
    ids = df['id'].values
    names = df['name'].values
    return {'labels':list(names),'values':list(ids)}

def get_classes_by_year(year):
    info = ALL_CLASSES.loc[ALL_CLASSES['class_year'] == year]
    mask = []
    for i in info['class_name'].values:
        if 'IB' in i:mask.append(False)
        else:mask.append(True)
    
    without_ib = info.iloc[mask][['class_id', 'class_term', 'class_name', 'grade_name']]
    without_ib.columns = ['id','term','name','grade_name']
    return without_ib

def get_classes_by_year_dic(year):
    df = get_classes_by_year(year)
    ids = df['id'].values
    names = df['name'].values
    return {'labels':list(names),'values':list(ids)}

#根据班级id获取，次班级所有的学生名单
#input: cla_id 'str'
#return: student_table 'dict'
#student_table: keys 学生id, values 学生姓名
def get_all_dict_by_class_id(cla_id):
    cla_id = int(cla_id)
    info = CUR_STUDENT.loc[CUR_STUDENT['class_id'] == cla_id]
    if info.empty:
        info = GRAD_STUDENT.loc[GRAD_STUDENT['class_id'] == cla_id]
        if info.empty: return None
    
    ids = info['id'].values
    names = info['name'].values
    student_table = {k:v for k,v in zip(ids,names)}
    return student_table
   

#已经CSV化
#根据班级id获取所有的考试分数
#input: cla_id 'str'
#return: 'pd.DataFrame'
#['student_id','exam_id','subject','score','z_score','t_score','r_score','div','class_rank']
def get_all_grade_by_class_id_total(cla_id):
    cla_id = int(cla_id)
    data = TOTAL_GRADE.loc[TOTAL_GRADE['class_id'] == cla_id].copy()
    subjects = [SUBJECTS[i] for i in data.subject_id.values]
    data['subject'] = subjects

    return data[['student_id','exam_id','subject','score','z_score','t_score','r_score','div','class_rank']]

#获取一个班级所有考试的最高分和最低分
#input: df 'pd.DataFrame'
#return: 'pd.DataFrame'
#{'subject','exam','exam_id','max','min'}
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
#input: cla_id 'str' 没有输入时获取全部数据
#return: 'pd.DataFrame'
#['student_id', 'student_name', 'class_id','subjects']
def sql_73(cla_id = None):
    if not cla_id:
        info = ALL_SUBJECT_73
    else:
        cla_id = int(cla_id)
        info = ALL_SUBJECT_73.loc[ALL_SUBJECT_73['class_id'] == cla_id]
    info = info[['student_id', 'student_name', 'class_id','subjects']]
    return info


def subject_of_teachers():
    info = LESSON.drop_duplicates('subject_id').values
    values = sorted(info)
    labels = [SUBJECTS[i] for i in values]
    return {'labels':labels, 'values':values}

def get_teacher_by_subject(subject_id):
    info = LESSON.loc[LESSON['subject_id'] == subject_id].drop_duplicates(subset = ['teacher_id'])
    ids = info.teacher_id.values
    names = info.teacher_name.values
    labels = ['编号:{0}, 姓名{1}'.format(str(i),j) for i,j in zip(ids,names)]
    return {'labels':labels, 'values':ids}