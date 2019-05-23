import pandas as pd
from models.globaltotal import SUBJECTS,CONTROLLER_TABLE,GRADETYPE,TOTAL_GRADE,TOTAL_TOTALS,EXAMS,CLASS_TABLE,CUR_STUDENT,GRAD_STUDENT,LESSON,CONTROLLER_INFO,STUDYDAYS,CONSUMPTION,CONSUMPTION_PREDICT,RANK_PREDICT

#简单的信息单行表同一返回以下结构的字典

#根据学生id获取在校生的基本信息
#input: stu_id  'int' 这里是在页面的回调函数里面转成了int，有空时统一一下
#return 'dict' {'index'：表头信息 'list'，'value'：学生基本信息, 'list'}
def get_student_info_by_student_id(stu_id):
    student = CUR_STUDENT.loc[CUR_STUDENT['id'] == stu_id].values
    index = ['学号','姓名','性别','民族','出生年份','家庭住址','家庭类型','班级编号','班级名称','班级学期','政治面貌','是否住校','是否退学','寝室号']
    student_info = {k:v for k,v in zip(index,student[0])}
    student_info['是否住校'] = '是' if student_info['是否住校'] else '否'
    student_info['是否退学'] = '是' if student_info['是否退学'] else '否'
    
    if not student_info['是否住校']: student_info['寝室号'] = '无'

    return {'index':index, 'value':list(student_info.values())}

#根据学生id获取毕业生的基本信息
#input: stu_id  'int' 这里是在页面的回调函数里面转成了int，有空时统一一下
#return 'dict' {'index'：表头信息 'list'，'value'：学生基本信息, 'list'}
def get_grad_student_info_by_student_id(stu_id):
    student = GRAD_STUDENT.loc[GRAD_STUDENT['id'] == stu_id].values
    index =['学号','姓名','班级编号','班级名称','班级学期']
    return {'index':index, 'value':student[0]}

#根据班级编号来获取所有班级的任课教师
#input: cla_id  'int' 这里是在页面的回调函数里面转成了int，有空时统一一下
#return 'dict' {'index'：表头信息 'list'，'value'：教师信息, 'list'}
def get_teachers_by_class_id(cla_id):
    lesson = LESSON.loc[LESSON['class_id'] == cla_id]
    subjects = lesson['subject_id'].values
    teachers = lesson['teacher_name'].values

    subjects = [SUBJECTS[i] for i in subjects]
    return {'index':subjects,'value':list(teachers)}

#根据学生id获取考勤信息
#input: stu_id 'str'
#return 'dict' {'id':学生id, 'data':考勤数据, 'type':考勤类型对照表}
def controller_info_by_student_id(stu_id):
    stu_id = int(stu_id)
    controller_info = CONTROLLER_INFO.loc[CONTROLLER_INFO['student_id'] == stu_id].copy()
    controller_info = controller_info.sort_values('id')
    controller_info['dates'] = pd.to_datetime(controller_info['date_time'], format='%Y/%m/%d %H:%M:%S')
    data = controller_info[['dates', 'type_id', 'term','class_name']]
    data.columns = ['dates','types','terms','class']

    return {'id':stu_id,'data':data,'type':CONTROLLER_TABLE}

#根据学生id获取消费信息
#input: stu_id 'str'
#return 'dict' {'id':学生id, 'data':消费数据}
# {id:student_id,data:[columns[date,time,money]]}
def consumption_by_student_id(stu_id):
    stu_id = int(stu_id)
    consumption_info = CONSUMPTION.loc[CONSUMPTION['student_id'] == stu_id]
    data = consumption_info[['date','time','money']]
    return {'id':stu_id,'data':data}

#根据学生id获取下月消费预测信息
#input: stu_id 'str'
#return 'list' [消费金额，警告类型]
def get_predict_consumption(stu_id):
    stu_id = int(stu_id)
    info = CONSUMPTION_PREDICT.loc[CONSUMPTION_PREDICT['student_id'] == stu_id]
    money = info['money'].values[0]
    warning = info['consumption_mode'].values[0]
    money = round(money,2)
    return [money,warning]

#根据学生id获取下次考试等第预测信息
#input: stu_id 'str'
#return: result 'dict' 
#result: keys 课程名称; values 等第的预测
def get_predict_rank(stu_id):
    stu_id = int(stu_id)

    info = RANK_PREDICT.loc[RANK_PREDICT['student_id'] == stu_id]
    subject = info['subject_id'].values
    rank = info['r_score'].values
    trend = info['trend'].values
    trends = {SUBJECTS[k]:v for k,v in zip(subject,trend)}
    result = {}
    for s,r in zip(subject,rank):
        #if s in [9,11,12]:continue
        if r < 0: r = 0.1 + (r/10)
        elif r > 1: r = 0.9 + (r-1)/10
        r = round(r,5)
        result[SUBJECTS[s]] = r
    return [result,trends]

#根据学期开始年份获取此年份学期的所有在校日数目
#input: year 'str'
#return: data list
def get_study_days_by_start_year(year):
    year = int(year)
    study_days = STUDYDAYS.loc[STUDYDAYS['year'] == year].values[0]
    data = study_days[1:]
    return data

def r_score_comment(r_score):
    if isinstance(r_score,str): return r_score
    if r_score <= 0.05:return '优秀'
    elif r_score <= 0.2:return '良好'
    elif r_score <= 0.4:return '中等'
    elif r_score <= 0.6:return '一般'
    else: return '后进'

#根据学生id获取考试分数
#input: stu_id 'str'
#return 'pd.DataFrame'
#{'test_id','exam_id','exam_name','subject_id','subject','score','z_score','t_score','r_score','mean','div','Grank','Crank'}
#div, 离均值;Grank, 年级排名;Crank, 班级排名
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
    Comments = []

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
        r_score = round(i[9],2) if i[9] != -6 else '考试状态异常'
        Rscores.append(r_score)
        Means.append(round(i[10],2) if i[10] != -1 else  '考试状态异常')
        Divs.append(round(i[11],2) if i[11] != -100 else '考试状态异常')
        G_ranks.append(round(i[12],2) if i[12] != -1 else '考试状态异常')
        C_ranks.append(round(i[13],2) if i[13] != -1 else '考试状态异常')
        Comments.append(r_score_comment(r_score))


    data = {'test_id':Test_ids,'exam_id':Exam_ids,'exam_name':Exam_names,'subject_id':Subject_ids,'subject':Subjects,
        'score':Scores,'z_score':Zscores,'t_score':Tscores,'r_score':Rscores,'mean':Means,'div':Divs,'Grank':G_ranks,'Crank':C_ranks,'Comment':Comments}

    return pd.DataFrame(data)

#根据学生id获取考试历次考试总分
#input: stu_id 'str'
#return 'pd.DataFrame'
#{'exam_name','total','mean','div','Grank','Crank'}
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

#由于绘制图表时需要在标题上加上学生信息，所以有了下面两个函数
def grade_query_res(stu_id):
    return {'id':stu_id,'data':get_student_grades_by_student_id(stu_id)}

def total_query_res(stu_id):
    return {'id':stu_id,'data':get_student_totals_by_student_id(stu_id)}

