from connect_db import student_data, course_data, select_table, add_schedule

# 判斷是否有衝堂
def check_schedule(SID, start, end):
    schedule_name = 'schedule_'+SID
    schedule = select_table(schedule_name)

    for i in range(start-1, end):
        if schedule[i][1] != None:
            return False            # 有衝堂
    return True                     # 無衝堂

def judge(SID, CID):
    student = student_data(SID)
    course = course_data(CID)

    if check_schedule(SID, course.start, course.end) == False:
        print('所選時段已有課程')
        return False

    #判斷是否達到最大人數
    elif course.max_member == course.current_member:
        print('人數已滿')
        return False

    #判斷是否為本系
    elif student.major != course.major and course.major != None:
        print('不可選修他系課程')
        return False

    #不可超過30學分
    elif student.total_credit + course.credit >= 30:
        print('學分已達上限')
        return False

    #判斷是否選擇同名課程
    elif course.course_id == 
        print('不可加選同一課程')
        return False

    
    return True

def add_course(SID, CID):
    if judge(SID, CID):
        add_schedule(SID, CID)
        print('加選成功')
    else:
        print('加選失敗')

# ========= test ===========

# SID = 'D1150459'
# CID = 1

# add_course(SID, CID)

# ==========================