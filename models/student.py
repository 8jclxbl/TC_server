from app import db
from models.models import CurStudent,GradStudent,ControllerInfo,Controller,Consumption,Class_,Lesson,Teacher,Subject,StudyDays
import pandas as pd


#简单的信息单行表同一返回以下结构的字典
#{'index'：表头信息，'value'：表中数据}
#根据学生id来获取学生的所有信息
def get_student_info_by_student_id(stu_id):
    student = db.session.query(CurStudent).filter_by(id = stu_id).first()
    class_info = db.session.query(Class_).filter_by(id = student.class_id).first()
    index = ['学号','姓名','性别','民族','出生年份','家庭住址','家庭类型','政治面貌','班级','班级编号','班级学期','是否住校','是否退学','寝室号']
    zhusu = '是' if student.zhusu else '否'
    tuixue = '是' if student.zhusu else '否'
    if not student.zhusu:qinshihao = '无'
    else: qinshihao = student.qinshihao
    value = [stu_id,student.name,student.sex,student.nation,student.born_year,student.native,student.residence,
                student.policy,class_info.name,student.class_id,class_info.term,zhusu,tuixue,qinshihao]
    return {'index':index, 'value':value}

def get_grad_student_info_by_student_id(stu_id):
    student = db.session.query(GradStudent).filter_by(id = stu_id).first()
    class_info = db.session.query(Class_).filter_by(id = student.class_id).first()
    index = ['学号','姓名','班级名称','班级编号','班级学期']
    value = [stu_id,student.name,class_info.name,student.class_id,class_info.term]
    return {'index':index, 'value':value}

#根据班级编号来获取所有班级的任课教师
def get_teachers_by_class_id(cla_id):
    lessons = db.session.query(Lesson).filter_by(class_id = cla_id).all()
    subjects_table = get_all_subject()

    subjects = []
    teachers = []
    for i in lessons:
        teacher = db.session.query(Teacher).filter_by(id = i.teacher_id).first()
        subjects.append(subjects_table[i.subject_id])
        teachers.append(teacher.name)
    return {'index':subjects,'value':teachers}

#获取全部的科目信息
def get_all_subject():
    subjects = db.session.query(Subject).all()
    sub_dic = {}
    for i in subjects:
        sub_dic[i.id] = i.name
    return sub_dic


def get_all_controller():
    controllers = db.session.query(Controller).all()
    controllers_table = {}
    for i in controllers:
        controllers_table[i.task_id] = i.name + ':' + i.task_name
    return controllers_table

#基于学生id查询考勤信息, type: int
def controller_info_by_student_id(id):
    infos = db.session.query(ControllerInfo).filter_by(student_id = id).all()
    type_table = get_all_controller()
    
    cur_info = infos[0]
    type_ids = [cur_info.type_id]
    dates = [cur_info.date_time]
    terms = [cur_info.Term]

    cla_info = db.session.query(Class_).filter_by(id = cur_info.class_id).first()
    class_ = [cla_info.name]

    cur_class = cur_info.class_id
    for i in infos[1:]:
        type_ids.append(i.type_id)
        dates.append(i.date_time)
        terms.append(i.Term)
        if i.class_id == cur_class:
            class_.append(cla_info.name)
        else:
            cla_info = db.session.query(Class_).filter_by(id = i.class_id).first()
            class_.append(cla_info.name)
            cur_class = i.class_id

    data = {'dates':dates,'types':type_ids,'terms':terms,'class':class_}
    return {'id':id,'data':pd.DataFrame(data),'type':type_table}


#以pd.dataframe的格式来输出查询结果
def consumption_by_student_id(id):
    infos = db.session.query(Consumption).filter_by(student_id = id).all()

    date = []
    time = []
    money = []
    text = []
    for i in infos:
        d,t = str(i.date_time).split(' ')
        m = i.money

        txt = str(i.date_time) + str(i.money)

        date.append(d)
        time.append(t)
        money.append(m)
        text.append(txt)

    data = {'date':date, 'time':time, 'money':money}
    return {'id':id,'data':pd.DataFrame(data),'text':text}

# {id:student_id,data:[columns[date,time,money]],text:total_info}

def get_study_days_by_start_year(year):
    info = db.session.query(StudyDays).filter_by(year = year).first()
    data = [info.term_one,info.term_two_first,info.term_two_second,info.term_two_trird]
    return data