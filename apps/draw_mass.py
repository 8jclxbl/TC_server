import dash_html_components as html 
import dash_core_components as dcc
import plotly.graph_objs as go 
from apps.simple_chart import dash_table


from app import app
from models.subject import get_all_grade_by_class_id,get_all_dict_by_class_id

import pandas as pd
import re

GRADETYPE = {-2:'缺考',-1:'作弊',-3:'免考'}

class Mass:
    #组织班级数据
    def __init__(self, query_res):
        self.data = query_res
        self.grade_sep()
        self.part_by_grade()
        self.class_obj = {}

    def grade_sep(self):
        temp = self.data['name'].values
        res_temp = []
        for i in temp:
            res_temp.append(re.search(r'\u9ad8.{1}',i).group())
        
        self.data.insert(0,'grade',res_temp)
        self.grades = list(set(res_temp))
        
    def part_by_grade(self):
        data = self.data
        grade_class = {}
        for i in self.grades:
            grade_class[i] = data.loc[data['grade'] == i][['id','name']]
        self.grade_class = grade_class

        class_id_name_by_grade = {}
        class_id_name = {}
        for i in self.grades:
            data = self.grade_class[i]
            dic = {}
            for j in data.values:
                dic[j[0]] = j[1]
            class_id_name_by_grade[i] = dic
            class_id_name.update(dic)
        self.class_id_name_by_grade = class_id_name_by_grade
        self.class_id_name = class_id_name

    def get_grades(self):
        return self.grades 

    def get_class_by_grade(self,grade):
        return self.grade_class[grade]

    def get_class_by_grade_dict(self,grade):
        return self.class_id_name_by_grade[grade]

    def get_class_name(self,cla_id):
        return self.class_id_name[cla_id]

    def get_one_class_by_grade(self,grade):
        return self.get_class_by_grade(grade)['id'].values[0]

    def get_all_class_objs_by_grade(self,grade):
        classes = self.grade_class[grade]
        class_ids = classes['id'].values

        temp = {}
        for i in class_ids:
            cla_info = ClassInfo(i)
            temp[i] = cla_info
        self.class_obj[grade] = temp

        return temp

    def get_mean_by_grade_exam(self,grade,exam_id,subject):
        classes = self.grade_class[grade]

        classes_ids = classes['id'].values
        classes_names = classes['name'].values

        classes_m = {}
        if grade not in self.class_obj:
            grade_class_objs = self.get_all_class_objs_by_grade(grade)
        else:
            grade_class_objs = self.class_obj[grade]
        for k,v in grade_class_objs.items():
            classes_m[k] = v.mean_grade(exam_id,subject)
        
        classes_mean = [round(classes_m[i],2) for i in classes_ids]
        return pd.DataFrame({'id':classes_ids,'name':classes_names,'mean':classes_mean})

    def get_rank_by_grade_exam(self,class_,grade,exam_id,subject):
        
        if grade not in self.class_obj:
            grade_class_objs = self.get_all_class_objs_by_grade(grade)
        else:
            grade_class_objs = self.class_obj[grade]

        if class_ not in grade_class_objs:
            class_info = ClassInfo(class_)
            self.class_obj[grade][class_] = class_info
        else:
            class_info = grade_class_objs[class_]
        
        return class_info.rank_grade(exam_id,subject)

    def get_partition_by_grade_exam(self,class_,grade,exam_id,subject):
        
        if grade not in self.class_obj:
            grade_class_objs = self.get_all_class_objs_by_grade(grade)
        else:
            grade_class_objs = self.class_obj[grade]
        
        if class_ not in grade_class_objs:
            class_info = ClassInfo(class_)
            self.class_obj[grade][class_] = class_info
        else:
            class_info = grade_class_objs[class_]

        return class_info.static_grade(exam_id,subject)

    

class ClassInfo:
    def __init__(self,cla_id):
        self.id = int(cla_id)
        self.get_grade()
        self.get_students()

    def get_students(self):
        self.students = get_all_dict_by_class_id(self.id)

    def get_grade(self):
        self.all_grade = get_all_grade_by_class_id(self.id)

    def get_exam(self):
        data = self.all_grade['exam_id'].values
        return sorted(list(set(data)))
        
    def get_exam_grade(self,exam_id):
        data = self.all_grade
        cur_data = data.loc[data['exam_id'] == exam_id]
        return cur_data

    def get_exam_subjects(self,exam_id):
        data = self.all_grade
        cur_data = data.loc[data['exam_id'] == exam_id]
        return list(cur_data['subject'].drop_duplicates().values)

    def mean_grade(self,exam_id,subject):
        data = self.get_exam_grade(exam_id)

        if subject != '总':
            data = data.loc[data['subject'] == subject]
        data = data.loc[data['score'] >= 0]
        if data.empty:return 0
        total_grade = data[['student_id','score']].groupby('student_id').sum()
        return total_grade['score'].mean()

    def rank_grade(self,exam_id,subject):
        data = self.get_exam_grade(exam_id)

        if subject != '总':
            data = data.loc[data['subject'] == subject]
            data = data.loc[data['score'] >= 0]
            data = data.sort_values('score',ascending = False)
            data.index = range(1,len(data) + 1)
            data['rank'] = data.index

            except_ = data.loc[data['score'] < 0]
            temp = except_.values
            temp = [GRADETYPE[i] for i in temp]
            except_['rank'] = temp
            return pd.concat([data,except_])
        else:
            data.loc[data['score'] < 0,'score'] = 0
            total = data[['student_id','name','score']].groupby('student_id').sum()
            total = total.sort_values('score',ascending = False)

            student_ids = total.index
            names = [self.students[i] for i in student_ids]
            scores = [i[0] for i in total.values]

            result = pd.DataFrame({'student_id':student_ids,'name':names,'score':scores})
            result['rank'] = range(1,len(result) + 1)

            return result

    def static_grade(self,exam_id,subject):
        data = self.get_exam_grade(exam_id)
        if data.empty:return None
        partition = {}
        if subject != '总':
            data = data.loc[data['subject'] == subject]
        
            data = data.loc[data['score'] >= 0]
            except_ = data.loc[data['score'] < 0]

            scores = data['score'].values

            except_score = except_['score'].values
            for i in except_score:
                if i not in partition:
                    partition[i] = 1
                else:
                    partition[i] += 1

        else:
            data.loc[data['score'] < 0,'score'] = 0
            total = data[['student_id','name','score']].groupby('student_id').sum()
            total = total.sort_values('score',ascending = False)

            scores = [i[0] for i in total.values]

        scores = sorted(scores,reverse = True)
        st = (scores[0] // 10) * 10
       
        for i in scores:
            if i < st:
                st -= 10
            if st not in partition:
                partition[st] = 1
            else:
                partition[st] += 1

        return partition


