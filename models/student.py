from app import session
from models.models import CurStudent,GradStudent,ControllerInfo,Consumption,Class_,Lesson,Teacher,StudyDays,ExamType,ConsumptionPredict,RankPredict
import pandas as pd

from models.globaltotal import SUBJECTS,CONTROLLER_TABLE,GRADETYPE,TOTAL_GRADE,TOTAL_TOTALS,EXAMS,CLASS_TABLE,ALL_CLASSES,CUR_STUDENT,GRAD_STUDENT,LESSON,CONTROLLER_INFO,STUDYDAYS,CONSUMPTION,CONSUMPTION_PREDICT,RANK_PREDICT


#简单的信息单行表同一返回以下结构的字典
#{'index'：表头信息，'value'：表中数据}
#根据学生id来获取学生的所有信息
"""def get_student_info_by_student_id(stu_id):
    student = session.query(CurStudent).filter_by(id = stu_id).first()
    class_info = ALL_CLASSES.loc[ALL_CLASSES['class_id'] == student.class_id]
    class_name = class_info['class_name'].values[0]
    class_term = class_info['class_term'].values[0]

    index = ['学号','姓名','性别','民族','出生年份','家庭住址','家庭类型','政治面貌','班级','班级编号','班级学期','是否住校','是否退学','寝室号']
    zhusu = '是' if student.zhusu else '否'
    tuixue = '是' if student.leave_school else '否'
    if not student.zhusu:qinshihao = '无'
    else: qinshihao = student.qinshihao

    value = [stu_id,student.name,student.sex,student.nation,student.born_year,student.native,student.residence,
                student.policy,class_name,student.class_id,class_term,zhusu,tuixue,qinshihao]

    #value = [stu_id,student.name,student.sex,student.nation,student.born_year,student.native,student.residence,
    #           student.policy,class_info.name,student.class_id,class_info.term,zhusu,tuixue,qinshihao]
    return {'index':index, 'value':value}
    
def get_grad_student_info_by_student_id(stu_id):
    student = session.query(GradStudent).filter_by(id = stu_id).first()
    class_info = ALL_CLASSES.loc[ALL_CLASSES['class_id'] == student.class_id]
    class_name = class_info['class_name'].values[0]
    class_term = class_info['class_term'].values[0]
    #class_info = session.query(Class_).filter_by(id = student.class_id).first()
    index = ['学号','姓名','班级名称','班级编号','班级学期']
    #value = [stu_id,student.name,class_info.name,student.class_id,class_info.term]
    value = [stu_id,student.name,class_name,student.class_id,class_term]
    return {'index':index, 'value':value}
    
#根据班级编号来获取所有班级的任课教师
def get_teachers_by_class_id(cla_id):
    lessons = session.query(Lesson).filter_by(class_id = cla_id).all()
    subjects_table = SUBJECTS

    subjects = []
    teachers = []
    for i in lessons:
        teacher = session.query(Teacher).filter_by(id = i.teacher_id).first()
        subjects.append(subjects_table[i.subject_id])
        teachers.append(teacher.name)
    return {'index':subjects,'value':teachers}

#基于学生id查询考勤信息, type: int
def controller_info_by_student_id(stu_id):
    infos = session.query(ControllerInfo).filter_by(student_id = stu_id).all()
    type_table = CONTROLLER_TABLE
    
    type_ids = []
    dates = []
    terms = []
    class_ = []

    cur_class_id = -1
    for i in infos:
        type_ids.append(i.type_id)
        dates.append(i.date_time)
        terms.append(i.Term)
        class_.append(CLASS_TABLE[i.class_id])

    #基于学生id查询考勤信息, type: int
def controller_info_by_student_id(stu_id):
    infos = session.query(ControllerInfo).filter_by(student_id = stu_id).all()
    type_table = CONTROLLER_TABLE
    
    type_ids = []
    dates = []
    terms = []
    class_ = []

    cur_class_id = -1
    for i in infos:
        type_ids.append(i.type_id)
        dates.append(i.date_time)
        terms.append(i.Term)
        class_.append(CLASS_TABLE[i.class_id])
            

    data = {'dates':dates,'types':type_ids,'terms':terms,'class':class_}
    return {'id':stu_id,'data':pd.DataFrame(data),'type':type_table}

    #以pd.dataframe的格式来输出查询结果
def consumption_by_student_id(stu_id):
    infos = session.query(Consumption).filter_by(student_id = stu_id).all()

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
    return {'id':stu_id,'data':pd.DataFrame(data),'text':text}
    """

def get_student_info_by_student_id(stu_id):
    student = CUR_STUDENT.loc[CUR_STUDENT['id'] == stu_id].values
    index = ['学号','姓名','性别','民族','出生年份','家庭住址','家庭类型','班级编号','班级名称','班级学期','政治面貌','是否住校','是否退学','寝室号']
    student_info = {k:v for k,v in zip(index,student[0])}
    student_info['是否住校'] = '是' if student_info['是否住校'] else '否'
    student_info['是否退学'] = '是' if student_info['是否退学'] else '否'
    
    if not student_info['是否住校']: student_info['寝室号'] = '无'

    return {'index':index, 'value':list(student_info.values())}

def get_grad_student_info_by_student_id(stu_id):
    student = GRAD_STUDENT.loc[GRAD_STUDENT['id'] == stu_id].values
    index =['学号','姓名','班级编号','班级名称','班级学期']
    return {'index':index, 'value':student[0]}

#根据班级编号来获取所有班级的任课教师
def get_teachers_by_class_id(cla_id):
    lesson = LESSON.loc[LESSON['class_id'] == cla_id]
    subjects = lesson['subject_id'].values
    teachers = lesson['teacher_name'].values

    subjects = [SUBJECTS[i] for i in subjects]
    return {'index':subjects,'value':list(teachers)}


def controller_info_by_student_id(stu_id):
    stu_id = int(stu_id)
    controller_info = CONTROLLER_INFO.loc[CONTROLLER_INFO['student_id'] == stu_id].copy()
    controller_info = controller_info.sort_values('id')
    controller_info['dates'] = pd.to_datetime(controller_info['date_time'], format='%Y/%m/%d %H:%M:%S')
    data = controller_info[['dates', 'type_id', 'term','class_name']]
    data.columns = ['dates','types','terms','class']

    return {'id':stu_id,'data':data,'type':CONTROLLER_TABLE}

#以pd.dataframe的格式来输出查询结果
def consumption_by_student_id(stu_id):
    stu_id = int(stu_id)
    consumption_info = CONSUMPTION.loc[CONSUMPTION['student_id'] == stu_id]
    data = consumption_info[['date','time','money']]
    return {'id':stu_id,'data':data}

# {id:student_id,data:[columns[date,time,money]],text:total_info}
def get_predict_consumption(stu_id):
    stu_id = int(stu_id)
    info = CONSUMPTION_PREDICT.loc[CONSUMPTION_PREDICT['student_id'] == stu_id]
    money = info['money'].values[0]
    warning = info['consumption_mode'].values[0]
    money = round(money,2)
    return [money,warning]

def get_predict_rank(stu_id):
    stu_id = int(stu_id)

    info = RANK_PREDICT.loc[RANK_PREDICT['student_id'] == stu_id]
    subject = info['subject_id'].values
    rank = info['r_score'].values
    result = {}
    for s,r in zip(subject,rank):
        if s in [9,11,12]:continue
        if r < 0: r = 0.1 + (r/10)
        elif r > 1: r = 0.9 + (r-1)/10
        r = round(r,5)
        result[SUBJECTS[s]] = r
    return result

def get_study_days_by_start_year(year):
    year = int(year)
    study_days = STUDYDAYS.loc[STUDYDAYS['year'] == year].values[0]
    data = study_days[1:]
    return data


def get_student_grades_by_student_id(stu_id):
    stu_id = int(stu_id)
    data = TOTAL_GRADE.loc[TOTAL_GRADE['student_id'] == stu_id].copy()
    data = data.sort_values('exam_id')

    Test_ids     = []
    Exam_ids     = []
    Exam_names   = []
    Subject_ids  = []
    Subjects     = []
    Scores       = []
    Zscores      = []
    Tscores      = []
    Rscores      = []
    Means        = []
    Divs         = []
    G_ranks      = []
    C_ranks      = []

    for i in data.values: 
        #if i[2] < 0:continue
        Test_ids.append(i[0])
        Exam_ids.append(i[1])
        Exam_names.append(EXAMS[i[1]])
        Subjects.append(SUBJECTS[i[2]])
        Subject_ids.append(i[2])
        Scores.append(i[6] if i[6] >= 0 else GRADETYPE[int(i[6])])
        Zscores.append(round(i[7],2) if i[7] != -6 else '考试状态异常')
        Tscores.append(round(i[8],2) if i[8] != -6 else '考试状态异常')
        Rscores.append(round(i[9],2) if i[9] != -6 else '考试状态异常')
        Means.append(round(i[10],2) if i[10] != -1 else  '考试状态异常')
        Divs.append(round(i[11],2) if i[11] != -100 else '考试状态异常')
        G_ranks.append(round(i[12],2) if i[12] != -1 else '考试状态异常')
        C_ranks.append(round(i[13],2) if i[13] != -1 else '考试状态异常')


    data = {'test_id':Test_ids,'exam_id':Exam_ids,'exam_name':Exam_names,'subject_id':Subject_ids,'subject':Subjects,
        'score':Scores,'z_score':Zscores,'t_score':Tscores,'r_score':Rscores,'mean':Means,'div':Divs,'Grank':G_ranks,'Crank':C_ranks}

    return pd.DataFrame(data)

def get_student_totals_by_student_id(stu_id):
    stu_id = int(stu_id)
    data = TOTAL_TOTALS.loc[TOTAL_TOTALS['stu_id'] == stu_id].copy()
    exams = []
    totals = []
    divs = []
    g_ranks = []
    c_ranks = []

    for i in data.values:
        exams.append(EXAMS[i[1]])
        totals.append(i[2])
        divs.append(round(i[7],2))
        g_ranks.append(i[5])
        c_ranks.append(i[8])

    data = {'exam_name':exams,'total':totals,'div':divs,'Grank':g_ranks,'Crank':c_ranks}
    return pd.DataFrame(data)

def grade_query_res(stu_id):
    return {'id':stu_id,'data':get_student_grades_by_student_id(stu_id)}

def total_query_res(stu_id):
    return {'id':stu_id,'data':get_student_totals_by_student_id(stu_id)}

