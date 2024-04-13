from init import Student, Course
from connect_db import student_data, course_data, remove_schedule

def withdraw_course(SID,CID):
    student = student_data(SID)
    course = course_data(CID)

    #判斷是否低於9學分
    if student.total_credit - course.credit < 9:
        error = '退選後不可小於9學分'
        return False, error
    elif course.type == '必修':
        error = '必修課須找助教協助手動退選'
        return False, error
    else:
        remove_schedule(SID, CID)
        return True, None

# ========= test ===========

# SID = 'D1150459'
# CID = 4

# withdraw_course(SID, CID)

# ==========================