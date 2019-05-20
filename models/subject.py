from models.globaltotal import SUBJECTS,NEED_PROCESS,CURRENT_THIRD,ELETIVE_CLASS,CLASS_TERMS,EXAMS,TOTAL_GRADE,ALL_CLASSES,CUR_STUDENT,GRAD_STUDENT,ALL_SUBJECT_73
import pandas as pd

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
        info = ALL_SUBJECT_73
    else:
        cla_id = int(cla_id)
        info = ALL_SUBJECT_73.loc[ALL_SUBJECT_73['class_id'] == cla_id]
    info = info[['student_id', 'student_name', 'class_id','subjects']]
    return info