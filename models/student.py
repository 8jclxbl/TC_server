from app import db
from models.models import CurStudent,ControllerInfo,Controller

#基于学生id查询考勤信息, type: int
def controller_info_by_student_id(id):
    infos = db.session.query(ControllerInfo).filter_by(student_id = id).all()
    types = Controller.query.all()

    type_dic = {}
    for i in types:
        type_dic[i.task_id] = i.task_name
    
    data = []
    for i in infos:
        record = {}
        record['type_id'] = i.type_id
        record['date'],record['time'] =  str(i.date_time).split(' ')
        data.append(record)


    return {'data':data,'type':type_dic}

    