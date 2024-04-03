from init import Student, Course
from connect_db import student_data, course_data, select_table, add_schedule

# 判斷是否有衝堂
def check_schedule(SID, start, end):
    schedule_name = 'schedule_'+SID
    schedule = select_table(schedule_name)

    for i in range(start-1, end):
        if schedule[i][1] != None:
            return False            # 有衝堂
    return True                     # 無衝堂


SID = 'D1150459'

student = student_data(SID)

print(student.SID)
print(student.name)
print(student.major)

CID = 1

course = course_data(CID)

print(course.cname)
print(course.major)

print(check_schedule(SID, course.start, course.end))

# flag = 1
# CID = '0002'
# if student_data.major != course_data.major and course_data.major != none
#     flag = 0