class Student:
    def __init__(self, SID, name, major):
        self.SID = SID                  # 學號
        self.name = name
        self.major = major

class Time:
    def __init__(self, ID, start_time, end_time):
        self.ID = ID
        self.start_time = start_time
        self.end_time = end_time

class Course:
    def __init__(self, ID, course_id, cname, professor, type, major, credit, max_member, current_member, start, end):
        self.ID = ID                    # 選課代碼
        self.course_id = course_id      # 課程代碼
        self.cname = cname              # 課堂名稱
        self.professor = professor      # 教授(id)
        self.type = type                # 必修/選修/通識
        self.major = major
        self.credit = credit            # 學分
        self.max_member = max_member
        self.current_member = current_member
        self.start = start              # 開始時間(id)
        self.end = end                  # 結束時間(id)

class Professor:
    def __init__(self, PID, name, major):
        self.PID = PID
        self.name = name
        self.major = major

class Schedule:
    def __init__(self, time_id, course_id):
        self.time_id = time_id
        self.course_id = course_id      # 選課代碼