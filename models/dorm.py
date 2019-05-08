from models.models import Sushe
from app import session


def get_dorm_by_class_id(cla_id):
    info = session.query(Sushe.sushe_id).filter_by(class_id = cla_id).all()
    info = [i[0] for i in info]
    return list(set(info))

def get_student_by_dorm_id(sushe_id,cla_id):
    info = session.query(Sushe.student_id).filter_by(sushe_id = sushe_id,class_id = cla_id).all()
    info = [i[0] for i in info]
    return info