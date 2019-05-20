from models.globaltotal import DORMS_INFO

def get_dorm_by_class_id(cla_id):
    cla_id = int(cla_id)
    info = DORMS_INFO.loc[DORMS_INFO['class_id'] == cla_id,'sushe_id'].drop_duplicates().values
    return list(info)

def get_student_by_dorm_id(sushe_id,cla_id):
    sushe_id = int(sushe_id)
    cla_id = int(cla_id)
    info = DORMS_INFO.loc[(DORMS_INFO['sushe_id'] == sushe_id) & (DORMS_INFO['class_id'] == cla_id), 'student_id'].values
    return list(info)