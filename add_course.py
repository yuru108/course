from init import Student, Course
from connect_db import student_data, course_data, update_course

SID = 'D1150459'

student = student_data(SID)

print(student.SID)
print(student.name)
print(student.major)

CID = 1

course = course_data(CID)

print(course.cname)
print(course.major)

# flag = 1
# CID = '0002'
# if student_data.major != course_data.major and course_data.major != none
#     flag = 0