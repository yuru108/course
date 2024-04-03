from connect_db import student_data

SID = 'D1150080'

print(student_data(SID))
print(student_data(SID)[0])
print(student_data(SID)[0][1])