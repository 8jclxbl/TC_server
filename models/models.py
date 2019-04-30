from app import db

#Teacher，Class，subject，Lesson用于表示1_teacher表中的内容
#教师表仅包含教师Id和Name
#另外建立班级表，学科表
#最后利用课程表将这三张表接连起来
class Teacher(db.Model):
    #bas_id
    id = db.Column(db.Integer, primary_key = True)
    #bas_name
    name = db.Column(db.String(32))

    def __repr__(self):
        return '<Teacher: {0}>'.format(self.name)
#班级
#Id，学期，年级， 名称
class Class_(db.Model):
    #cla_id
    id = db.Column(db.Integer, primary_key = True)
    #应和Lesson里对应的Term一致。。。 这里还是用唯一ID标识，尽量少些数据
    term = db.Column(db.String(16))
    #gra_Name，年纪数据可以由班级名称得到
    #Grade = db.Column(db.String(32))
    #cla_Name
    name = db.Column(db.String(32))
    def __repr__(self):
        return '<Class_: {0}>'.format(self.name)

#学科
#Id，名称
class Subject(db.Model):
    #sub_id
    id = db.Column(db.Integer, primary_key = True)
    #sub_Name
    name = db.Column(db.String(32))
    def __repr__(self):
        return '<Subject: {0}>'.format(self.name)

#课程
#Id
class Lesson(db.Model):
    #表内编号，一个实例代表teacher表中的一行
    id = db.Column(db.Integer, primary_key = True)
    #term
    #term = db.Column(db.String(16))
    #课程的学科Id
    #SubjectId = db.Column(db.Integer,db.ForeignKey('subject.Id'))
    subject_id = db.Column(db.Integer)
    #subject = db.relationship('Subject',back_populates='lesson')
    #课程的老师Id
    #TeacherId = db.Column(db.Integer,db.ForeignKey('teacher.Id'))
    teacher_id = db.Column(db.Integer)
    #teacher = db.relationship('Teacher',back_populates='lesson')
    #课程的班级Id
    #ClassId = db.Column(db.Integer,db.ForeignKey('class_.Id'))
    class_id = db.Column(db.Integer)
    #class_ = db.relationship('Class_',back_populates='lesson')
    def __repr__(self):
        return '<Lesson: {0}>'.format(self.id)


#学生信息类，用于表述2_student_info.csv
class CurStudent(db.Model):
    #bf_StudentID
    id = db.Column(db.Integer, primary_key = True)
    #bf_Name
    name = db.Column(db.String(32))
    #bf_sex
    #sex = db.Column(db.Boolean)
    sex = db.Column(db.String(8))
    #bf_nation
    nation = db.Column(db.String(16))
    #bf_BornDate
    born_year = db.Column(db.String(16))
    #bf_NativePlace
    native = db.Column(db.String(16))

    #确认此列数据全是城镇
    residence = db.Column(db.String(16))
    #cla_id:同上面的class表相关联
    #ClassId = db.Column(db.Integer, db.ForeignKey('class_.Id'))
    class_id = db.Column(db.Integer)
    #class_ = db.relationship('Class_',back_populates='student')
    #bf_policy
    policy = db.Column(db.String(16))
    #Bf_ResidenceType 
    #bf_zhusu
    zhusu = db.Column(db.Boolean)
    #bf_leaveSchool
    leave_school = db.Column(db.Boolean)
    #bf_qinshihao
    qinshihao = db.Column(db.Integer)

    def __repr__(self):
        return '<CurStudent: {0}>'.format(self.name)

class GradStudent(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    #bf_Name
    name = db.Column(db.String(32))
    class_id = db.Column(db.Integer)

    def __repr__(self):
        return '<GradStudent: {0}>'.format(self.name)

class Consumption(db.Model):
    #自增主键
    id = db.Column(db.Integer, primary_key = True)
    #DealTime
    date_time = db.Column(db.DateTime)
    #MonDel
    money = db.Column(db.Float)
    #bf_StudentID
    #StudentId = db.Column(db.Integer,db.ForeignKey('student.Id'))
    student_id = db.Column(db.Integer)
    #student = db.relationship('Student', back_populates = 'consumption')

    def __repr__(self):
        return '<Consumption: {0}>'.format(self.date_time)

#此类记录4_kaoqintype.csv
class Controller(db.Model):
    #controler_id
    id = db.Column(db.Integer)
    #controler_name
    name = db.Column(db.String(32))

    #control_task_order_id
    task_id =  db.Column(db.Integer,primary_key = True)
    #control_task_name
    task_name = db.Column(db.String(32))

    def __repr__(self):
        return '<Controller: {0}>'.format(self.name)

#此类记录3_kaoqin.csv
class ControllerInfo(db.Model):
    #kaoqing_id
    id = db.Column(db.Integer, primary_key = True)
    #qj_term
    Term = db.Column(db.String(16))
    #DataDateTime
    date_time = db.Column(db.DateTime)
    
    #ControllerID
    #通过此Id和Controller类的数据关联
    #TypeId = db.Column(db.Integer, db.ForeignKey('controller.TaskId'))
    type_id = db.Column(db.Integer)
    #type_ = db.relationship('Controller', back_populates = 'controller_info')
    
    #用班级ID和班级表关联
    #ClassId = db.Column(db.Integer,db.ForeignKey('class_.Id'))
    class_id = db.Column(db.Integer)
    #class_ = db.relationship('Class_',back_populates='controller_info')
    
    #这里直接记录而不是直接用Id和student类关联的原因是
    #二者数据部分对不上，考勤中记录的学生好像更多
    student_id = db.Column(db.Integer)
    #StudentName = db.Column(db.String(16))

    def __repr__(self):
        return '<ControllerInfo: {0}>'.format(self.id)


class StudyDays(db.Model):
    year = db.Column(db.Integer,primary_key = True)
    term_one = db.Column(db.Integer)
    term_two_first =  db.Column(db.Integer)
    term_two_second =  db.Column(db.Integer)
    term_two_trird =  db.Column(db.Integer)

class Exam(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))
    term = db.Column(db.String(16))
    type_id = db.Column(db.Integer)
    date_time = db.Column(db.DateTime)

class ExamType(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(64))

class ExamRes(db.Model):
    id = db.Column(db.Integer, primary_key = True)
    test_id = db.Column(db.Integer)
    exam_id = db.Column(db.Integer)
    subject_id = db.Column(db.Integer)
    student_id = db.Column(db.Integer)
    score = db.Column(db.Float)
    z_score = db.Column(db.Float)
    t_score = db.Column(db.Float)
    r_score = db.Column(db.Float)

