from connect_db import student_data, course_data, select_table, add_schedule
from search import same_course

# 判斷是否有衝堂
def check_schedule(SID, start, end):
    schedule_name = 'schedule_'+SID
    schedule = select_table(schedule_name)

    for i in range(start-1, end):
        if schedule[i][1] != None:
            return False            # 有衝堂
    return True                     # 無衝堂

def add_course(SID, CID):
    student = student_data(SID)
    course = course_data(CID)

    if check_schedule(SID, course.start, course.end) == False:
        error = '所選時段已有課程'
        return False, error

    #判斷是否達到最大人數
    elif course.max_member == course.current_member:
        error = '人數已滿'
        return False, error

    #判斷是否為本系
    elif student.major != course.major and course.major != '通識學院':
        error = '不可選修他系課程'
        return False, error

    #不可超過30學分
    elif student.total_credit + course.credit >= 30:
        error = '學分已達上限'
        return False, error

    #判斷是否選擇同名課程
    elif same_course(student.SID, course.course_id):
        error = '不可加選同一課程'
        return False, error
    
    else:
        add_schedule(SID, CID)
        return True, None

# ========= test ===========

# SID = 'D1150459'
# CID = 4

# add_course(SID, CID)

# ==========================