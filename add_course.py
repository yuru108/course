from connect_db import student_data,select_table,init_course
from init import Student

SID = 'D1150459'

student = student_data(SID)

print(student.SID)
print(student.name)
print(student.major)

# flag = 1
# CID = '0002'
# if student_data.major != course_data.major and course_data.major != none
#     flag = 0
    
