import pandas as pd
from models.globaltotal import TOTAL_GRADE,EXAMS,SUBJECTS,LESSON
from models.subject import get_all_grade_by_class_id_total

def get_exams_by_year_grade(year,grade):
    info = TOTAL_GRADE[['year','grade','exam_id']].loc[(TOTAL_GRADE['year'] == year) & (TOTAL_GRADE['grade'] == grade)]
    exams = info['exam_id'].drop_duplicates().values
    names = [EXAMS[i] for i in exams]
    return {'labels':names, 'values':exams}

def get_subject_by_year_grade_exam(year,grade,exam):
    info = TOTAL_GRADE[['year','grade','exam_id','subject_id']].loc[(TOTAL_GRADE['exam_id'] == exam) & (TOTAL_GRADE['year'] == year) & (TOTAL_GRADE['grade'] == grade)]
    subjects = info['subject_id'].drop_duplicates().values
    names = [SUBJECTS[i] for i in subjects]
    return {'labels':names, 'values':subjects}

def get_grades_by_year_grade_subject(year, grade,exam,subject):
    print(year, grade,exam,subject)
    #info = LESSON.loc[(LESSON['term_year'] == year)]
    info = LESSON.loc[(LESSON['term_year'] == year) & (LESSON['grade_name'] == grade) & (LESSON['subject_id'] == subject)]
    classes = info['class_id'].values
    teachers = info['teacher_id'].values
    
    means = []
    for i in classes:
        means.append(get_all_class_mean_by_subject(year,grade,i,subject,exam))

    res = {k:v for k,v in zip(teachers,means)}
    return res

def get_all_class_mean_by_subject(year,grade,cla_id,subject,exam):
    cla_id = int(cla_id)
    mean = TOTAL_GRADE.loc[(TOTAL_GRADE['class_id'] == cla_id) & (TOTAL_GRADE['year'] == year) & (TOTAL_GRADE['grade'] == grade) & (TOTAL_GRADE['subject_id'] == subject) & (TOTAL_GRADE['exam_id'] == exam), 'score'].mean()
    return mean