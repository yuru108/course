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

#判斷是否為本系
if student.major != course.major and course.major != None:
    print('ERROR!')

#判斷是否達到最大人數
elif course.max_member == course.current_member:
    print('FULL')

#判斷是否選擇同名課程
else:
    for i in range(1, 70):
        if Schedule[i][1].course_id == course.course_id:
            print('ERROR')

#不可超過30學分
    credit = 0
    for i in range(1,70):
        course = Schedule[i][1].course_id
        credit += course.course_id
    if  course.credit + course.course_id >= 30:
            print('ERROR')


