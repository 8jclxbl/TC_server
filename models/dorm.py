from models.globaltotal import DORMS_INFO

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
