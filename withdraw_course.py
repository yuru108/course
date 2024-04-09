from init import Student, Course
from connect_db import student_data, course_data, select_table, add_schedule

def judge(SID,CID):
    student = student_data(SID)
    course = course_data(CID)

    #判斷是否低於9學分
    if student.total_credit - course.credit < 9:
        print('退選後不可小於9學分')
        return False
    elif course.type == 1:
        print('警告，是否要退選必修課?')