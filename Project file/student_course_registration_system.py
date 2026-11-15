# Student Course Registration System (PS No. 90)
# Made using topics from the Python syllabus:
# variables, type casting, operators, if-elif-else, loops, functions, lambda,
# strings (f-strings, format()), tuples, lists, list comprehension,
# dictionaries, dictionary comprehension, sets, exception handling, file handling

FILE_NAME = "registrations.txt"   
MAX_COURSES = 3                   



class Course:
    def __init__(self, code, name, capacity):
        self.code = code                
        self.name = name                
        self.capacity = capacity        
        self.enrolled = set()           

    def seats_left(self):
        return self.capacity - len(self.enrolled)   


class Student:
    def __init__(self, sid, name):
        self.sid = sid                  
        self.name = name                
        self.courses = []               


COURSE_DATA = (
    ("CS101", "Programming", 2),
    ("MA101", "Mathematics", 30),
    ("PH101", "Physics", 30),
)


courses = {code: Course(code, name, cap) for code, name, cap in COURSE_DATA}


students = {}


def save_file():
    f = open(FILE_NAME, "w")                        
    try:
        for s in students.values():                
            for code in s.courses:                  
                f.write(f"{s.sid},{s.name},{code}\n")   #
    finally:
        f.close()                                   


def load_file():
    try:
        f = open(FILE_NAME, "r")                    
    except FileNotFoundError:
        pass                                       
    else:                                           
        for line in f:
            line = line.strip()                    
            if line == "":
                continue                            
            sid, name, code = line.split(",")       
            if sid not in students:
                students[sid] = Student(sid, name)  
            students[sid].courses.append(code)      
            courses[code].enrolled.add(sid)        
        f.close()


def register():
    sid = input("Student ID: ").strip()
    name = input("Name: ").strip()
    code = input("Course: ").strip().upper()

    # check 1: course must exist
    if code not in courses:
        print(f"Course {code} does not exist.")
        return

    course = courses[code]
    student = students.get(sid)                    

    # check 2: no duplicate registration
    if student is not None and code in student.courses:
        print(f"Student {sid} is already registered in {code}.")
        return

    # check 3: course must have free seats
    if course.seats_left() == 0:
        print(f"Course {code} is full.")
        return

    # check 4: not more than 3 courses per student
    if student is not None and len(student.courses) >= MAX_COURSES:
        print(f"Student {sid} cannot register for more than {MAX_COURSES} courses.")
        return

    # all checks passed
    if student is None:
        student = Student(sid, name)                
        students[sid] = student
    student.courses.append(code)                   
    course.enrolled.add(sid)                        
    save_file()                                    

    print(f"Registered: {student.name} ({sid}) in {code} - {course.name}.")
    print(f"Seats left: {course.seats_left()}")


def drop_course():
    sid = input("Student ID: ").strip()
    code = input("Course: ").strip().upper()

    if sid not in students:
        print(f"Student {sid} not found.")
        return
    if code not in courses:
        print(f"Course {code} does not exist.")
        return

    student = students[sid]
    if code not in student.courses:
        print(f"Student {sid} is not registered in {code}.")
        return

    student.courses.remove(code)                    
    courses[code].enrolled.remove(sid)              
    save_file()                                     

    print(f"{student.name} ({sid}) dropped {code}. Seats left: {courses[code].seats_left()}")


def view_student():
    sid = input("Student ID: ").strip()

    if sid not in students:
        print(f"Student {sid} not found.")
        return

    student = students[sid]
    if len(student.courses) == 0:
        print(f"{student.name} ({sid}) has no registered courses.")
    else:
        
        lines = [f"{c} - {courses[c].name}" for c in student.courses]
        print(f"{student.name} ({sid}) is registered in:")
        for line in lines:
            print(line)


def view_course_list():
    
    for course in sorted(courses.values(), key=lambda c: c.code):
        
        print("{} - {} | seats left: {}".format(course.code, course.name, course.seats_left()))


def common_students():
    code1 = input("First course: ").strip().upper()
    code2 = input("Second course: ").strip().upper()

    if code1 not in courses or code2 not in courses:
        print("One of the courses does not exist.")
        return


    common = courses[code1].enrolled & courses[code2].enrolled
    if len(common) == 0:
        print(f"No student is registered in both {code1} and {code2}.")
    else:
        for sid in sorted(common):
            print(f"{students[sid].name} ({sid})")



load_file()                                         

while True:
    print("")
    print("1. Register")
    print("2. View student")
    print("3. Drop course")
    print("4. View course list")
    print("5. Students in two courses")
    print("6. Exit")

    try:
        choice = int(input("Menu: "))               
    except ValueError:
        print("Please enter a number from 1 to 6.")
        continue                                    

    if choice == 1:
        register()
    elif choice == 2:
        view_student()
    elif choice == 3:
        drop_course()
    elif choice == 4:
        view_course_list()
    elif choice == 5:
        common_students()
    elif choice == 6:
        break                                       
    else:
        print("Invalid choice")