from init import Student, Course
from connect_db import student_data, course_data, remove_schedule

def judge(SID,CID):
    student = student_data(SID)
    course = course_data(CID)

    #判斷是否低於9學分
    if student.total_credit - course.credit < 9:
        print('退選後不可小於9學分')
        return False
    elif course.type == '必修':
        print('警告，是否要退選必修課?')
        return False
    return True

def withdraw_course(SID, CID):
    if judge(SID, CID):
        remove_schedule(SID, CID)
        print('退選成功')
    else:
        print('退選失敗')

# ========= test ===========

# SID = 'D1150459'
# CID = 4

# withdraw_course(SID, CID)

# ==========================