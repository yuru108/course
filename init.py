class Student:
    def __init__(self, SID, name, major):
        self.SID = SID
        self.name = name
        self.major = major

class Time:
    def __init__(self, ID, start_time, end_time):
        self.ID = ID
        self.start_time = start_time
        self.end_time = end_time

class Course:
    def __init__(self, ID, course_id, cname, professor, type, major, credit, max_member, current_member, start, end):
        self.ID = ID
        self.course_id = course_id
        self.cname = cname
        self.professor = professor
        self.type = type
        self.major = major
        self.credit = credit
        self.max_member = max_member
        self.current_member = current_member
        self.start = start
        self.end = end

class Professor:
    def __init__(self, PID, name, major):
        self.PID = PID
        self.name = name
        self.major = major

class Schedule:
    def __init__(self, time_id, course_id):
        self.time_id = time_id
        self.course_id = course_id