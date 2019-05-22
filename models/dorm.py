from models.globaltotal import DORMS_INFO,TOTAL_GRADE,SUBJECTS

#基于班级id获取班级的所有的宿舍的列表
#input: cla_id 'str' 直接从下拉菜单中获取的，字符串类型，函数中会先转 int
#return: 'list' 
def get_dorm_by_class_id(cla_id):
    cla_id = int(cla_id)
    info = DORMS_INFO.loc[DORMS_INFO['class_id'] == cla_id,'sushe_id'].drop_duplicates().values
    return list(info)

#基于班级id和宿舍id获取此宿舍所有的学生的id
#input: sushe_id, 宿舍id 'str'; cla_id  班级id 'str'
#return: 'list'
def get_student_by_dorm_id(sushe_id,cla_id):
    sushe_id = int(sushe_id)
    cla_id = int(cla_id)
    info = DORMS_INFO.loc[(DORMS_INFO['sushe_id'] == sushe_id) & (DORMS_INFO['class_id'] == cla_id), 'student_id'].values
    return list(info)

def get_grade_subjects(sushe_id,cla_id):
    students = get_student_by_dorm_id(sushe_id,cla_id)
    all_subjects = []
    for i in students:
        subjects = TOTAL_GRADE.loc[TOTAL_GRADE['student_id'] == i,'subject_id'].values
        all_subjects += list(subjects)
    all_subjects = set(all_subjects)
    if -1 in all_subjects: all_subjects.remove(-1)
    all_subjects = sorted(list(all_subjects))
    all_subjects_name = [SUBJECTS[i] for i in all_subjects]
    return {'labels':all_subjects_name, 'values':all_subjects}