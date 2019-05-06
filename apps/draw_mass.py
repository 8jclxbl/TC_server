import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go 
from apps.simple_chart import dash_table


from app import app
from models.subject import get_all_grade_by_class_id,get_all_dict_by_class_id

import pandas as pd
import re

GRADETYPE = {-2:'缺考',-1:'作弊',-3:'免考'}
GENERE_EXAM_ID = [285,287,291,297,303,305]

def static_header_trans(static_res,exam_id):
    if exam_id in GENERE_EXAM_ID:step = 4
    else:step = 9
    head = static_res.keys()
    head = sorted(head)
    header = []
    value = []
    for i in head:
        if i > 0:
            if step == 4 and i == 10:header.append('10-15')
            else:
                header.append('{0}-{1}'.format(i,i+step))
        elif i == 0:header.append('0')
        else:
            header.append(GRADETYPE[i])
        value.append(static_res[i])
    return [header,value]

class Mass:
    #组织班级数据
    def __init__(self, query_res):
        #输入数据为，根据学期查询的班级数据
        self.data = query_res
        
        self.grade_sep()
        self.part_by_grade()
        self.class_obj = {}

    def grade_sep(self):
        #获取当前学期所有班级的名称
        temp = self.data['name'].values
        res_temp = []
        for i in temp:
            #利用正则表达式获取当前的年级
            res_temp.append(re.search(r'\u9ad8.{1}',i).group())
        
        #将年级数据置入数据表中
        self.data.insert(0,'grade',res_temp)

        #此学期的年级数据
        self.grades = list(set(res_temp))
        
    def part_by_grade(self):
        #根据年级划分数据
        data = self.data
        #暂存各年级数据的字典
        grade_class = {}
        #将数据整合成字典结构{年级{班级id：班级名称}}
        for i in self.data.values:
            if i[0] not in grade_class:
                grade_class[i[0]] = {i[1]:i[3]}
            else:
                grade_class[i[0]].update({i[1]:i[3]})
        self.grade_class = grade_class

    #获取当前对象中所包含的年级
    def get_grades(self):
        return self.grades 

    #根据年级获取当前年级的数据
    def get_class_by_grade_dict(self,grade):
        return self.grade_class[grade]

    #提取某一个班以获取当前年级的考试数据
    def get_one_class_by_grade(self,grade):
        return list(self.grade_class[grade].keys())[0]

    #根据年级生成其所有的班级数据
    def get_all_class_objs_by_grade(self,grade):
        classes = self.grade_class[grade]
        class_ids = classes.keys()
        temp = {}
        for i in class_ids:
            cla_info = ClassInfo(i)
            temp[i] = cla_info
        self.class_obj[grade] = temp
        return temp

    #计算各年级的各次考试的均分
    def get_mean_by_grade_exam(self,grade,exam_id,subject):
        #获取当前年级的所有班级
        classes = self.grade_class[grade]

        #获取当前年级的所有班级id和名称
        classes_ids = list(classes.keys())
        classes_names = list(classes.values())

        #记录当前班级当前学科的均分
        classes_m = {}

        #若并未生成当前年级的成绩对象，则生成，否则直接使用
        if grade not in self.class_obj:
            grade_class_objs = self.get_all_class_objs_by_grade(grade)
        else:
            grade_class_objs = self.class_obj[grade]

        #利用对应的年级对象生成所有的均值数据
        for k,v in grade_class_objs.items():
            classes_m[k] = v.mean_grade(exam_id,subject)
        
        #对均值数据取两位小数
        classes_mean = [round(classes_m[i],2) for i in classes_ids]
        #生成一个pd.dataframe对象便于画图
        return pd.DataFrame({'id':classes_ids,'name':classes_names,'mean':classes_mean})

#班级信息
class ClassInfo:
    def __init__(self,cla_id):
        #记录班级id
        self.id = int(cla_id)
        #这里的grade均是成绩的意思
        #获取成绩
        self.get_grade()
        #获取本版所有学生
        self.get_students()

    #根据班级id获取班级的所有学生
    def get_students(self):
        self.students = get_all_dict_by_class_id(self.id)

    #根据班级id获取本班的所有考试的成绩
    def get_grade(self):
        self.all_grade = get_all_grade_by_class_id(self.id)

    #获取本班的所有考试
    def get_exam(self):
        data = self.all_grade['exam_id'].values
        return sorted(list(set(data)))
        
    #获取此次考试的所有数据
    def get_exam_grade(self,exam_id):
        data = self.all_grade
        cur_data = data.loc[data['exam_id'] == exam_id]
        return cur_data.copy()

    #获取此次考试的所有学科
    def get_exam_subjects(self,exam_id):
        data = self.all_grade
        cur_data = data.loc[data['exam_id'] == exam_id]
        return list(cur_data['subject'].drop_duplicates().values)

    #计算某次考试某一学科的均值
    def mean_grade(self,exam_id,subject):
        data = self.get_exam_grade(exam_id)
        if subject != '总':
            data = data.loc[data['subject'] == subject]
        data = data.loc[data['score'] >= 0]
        if data.empty:return 0
        total_grade = data[['student_id','score']].groupby('student_id').sum()
        return total_grade['score'].mean()

    #计算本次考试的班内排名
    def rank_grade(self,exam_id,subject):
        #注意，很多时候这样获取值，可能知识得到指定的pd.DataFrame对象的一个view
        #此时，改变对象的值可能引起原始的值的变化，为了避免这种情况触发的warning
        #这里直接指定数据是原始对象的一个copy
        data = self.get_exam_grade(exam_id)

        #对于非总分数据，计算排名时只需要把异常的考试状态排在最后面即可
        if subject != '总':
            data = data.loc[data['subject'] == subject]

            normal = data.loc[data['score'] >= 0]
            normal = normal.sort_values('score',ascending = False)
            normal.index = range(1,len(normal) + 1)
            normal['rank'] = normal.index

            except_ = data.loc[data['score'] < 0].copy()
            temp = except_.values
            temp = [GRADETYPE[i[4]] for i in temp]
            except_['rank'] = temp
            return pd.concat([normal,except_])
        else:
            #由于要计算总分，为了避免异常状态的影响，均记为0

            #如果前面不指定copy,此处的赋值操作会一直warning
            data.loc[data.score < 0,'score'] = 0
            total = data[['student_id','name','score']].groupby('student_id').sum()
            total = total.sort_values('score',ascending = False)

            student_ids = total.index
            names = [self.students[i] for i in student_ids]
            scores = [round(i[0],2) for i in total.values]

            result = pd.DataFrame({'student_id':student_ids,'name':names,'score':scores})
            result['rank'] = range(1,len(result) + 1)

            return result

    def static_grade(self,exam_id,subject):
        #分数统计，和排名差不多
        data = self.get_exam_grade(exam_id)
        if data.empty:return None
        partition = {}
        if subject != '总':
            data = data.loc[data['subject'] == subject]
            normal = data.loc[data['score'] >= 0]
            except_ = data.loc[data['score'] < 0]

            scores = normal['score'].values
            except_score = except_['score'].values
            for i in except_score:
                if i not in partition:
                    partition[i] = 1
                else:
                    partition[i] += 1

        else:
            data.loc[data.score < 0,'score'] = 0
            total = data[['student_id','name','score']].groupby('student_id').sum()
            total = total.sort_values('score',ascending = False)
            scores = [i[0] for i in total.values]

        if len(scores) == 0: return None
        scores = sorted(scores,reverse = True)

        if subject != '总' and exam_id in GENERE_EXAM_ID:
            level = 10
            for i in scores:
                if i < level:
                    level -= 5
                if level not in partition:
                    partition[level] = 1
                else:
                    partition[level] += 1
            return partition

        st = (scores[0] // 10) * 10

        for i in scores:
            if i == 0:
                if i not in partition:partition[0] = 1
                else: partition[0] += 1
            if i < st:
                st -= 10
            if st not in partition:
                partition[st] = 1
            else:
                partition[st] += 1

        return partition


