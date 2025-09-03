import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import tkinter.font as tkFont # Import tkFont for custom font definitions

# ############################################################################
#
# MODEL
#
# The classes below are based on the provided project description.
# (No changes needed in the model part as the request is UI-related)
# ############################################################################

class Person:
    def __init__(self, id, name):
        self._id = id
        self._name = name

    @property
    def id(self):
        return self._id

    @property
    def name(self):
        return self._name

    def to_dict(self):
        raise NotImplementedError

class Student(Person):
    def __init__(self, id, name, major):
        super().__init__(id, name)
        self._major = major
        self._enrolled_course_codes = []

    @property
    def major(self):
        return self._major

    @major.setter
    def major(self, major):
        self._major = major

    @property
    def enrolled_course_codes(self):
        return self._enrolled_course_codes

    def enroll_course(self, course_code):
        if course_code not in self._enrolled_course_codes:
            self._enrolled_course_codes.append(course_code)

    def drop_course(self, course_code):
        if course_code in self._enrolled_course_codes:
            self._enrolled_course_codes.remove(course_code)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "major": self.major,
            "enrolled_courses": self.enrolled_course_codes,
            "type": "student",
        }

class Faculty(Person):
    def __init__(self, id, name, department):
        super().__init__(id, name)
        self._department = department
        self._assigned_course_codes = []

    @property
    def department(self):
        return self._department

    @department.setter
    def department(self, department):
        self._department = department

    @property
    def assigned_course_codes(self):
        return self._assigned_course_codes

    def assign_course(self, course_code):
        if course_code not in self._assigned_course_codes:
            self._assigned_course_codes.append(course_code)

    def unassign_course(self, course_code):
        if course_code in self._assigned_course_codes:
            self._assigned_course_codes.remove(course_code)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "department": self.department,
            "assigned_courses": self.assigned_course_codes,
            "type": "faculty",
        }

class Course:
    def __init__(self, course_code, title, credits, prerequisites=None):
        self._course_code = course_code
        self._title = title
        self._credits = credits
        self._prerequisite_codes = prerequisites if prerequisites else []
        self._enrolled_student_ids = []
        self._assigned_faculty_id = None

    @property
    def course_code(self):
        return self._course_code

    @property
    def title(self):
        return self._title
    
    @property
    def credits(self):
        return self._credits

    @property
    def prerequisite_codes(self):
        return self._prerequisite_codes

    @property
    def enrolled_student_ids(self):
        return self._enrolled_student_ids

    @property
    def assigned_faculty_id(self):
        return self._assigned_faculty_id

    @assigned_faculty_id.setter
    def assigned_faculty_id(self, faculty_id):
        self._assigned_faculty_id = faculty_id

    def add_student_id(self, student_id):
        if student_id not in self._enrolled_student_ids:
            self._enrolled_student_ids.append(student_id)

    def remove_student_id(self, student_id):
        if student_id in self._enrolled_student_ids:
            self._enrolled_student_ids.remove(student_id)

    def to_dict(self):
        return {
            "course_code": self.course_code,
            "title": self.title,
            "credits": self.credits,
            "prerequisites": self.prerequisite_codes,
            "enrolled_students": self.enrolled_student_ids,
            "faculty_id": self.assigned_faculty_id,
        }

class University:
    def __init__(self):
        self._students = []
        self._faculty = []
        self._courses = []

    def add_student(self, student):
        if not any(s.id == student.id for s in self._students):
            self._students.append(student)
            return True
        return False

    def get_student(self, student_id):
        for student in self._students:
            if student.id == student_id:
                return student
        return None

    def get_all_students(self):
        return self._students.copy()
    
    # New: Remove student and their enrollments
    def remove_student(self, student_id):
        student_to_remove = self.get_student(student_id)
        if student_to_remove:
            # Remove student from all courses they are enrolled in
            for course in self._courses:
                if student_id in course.enrolled_student_ids:
                    course.remove_student_id(student_id)
                    student_to_remove.drop_course(course.course_code) # Also update student's own list
            self._students.remove(student_to_remove)
            return True
        return False

    def add_faculty(self, faculty):
        if not any(f.id == faculty.id for f in self._faculty):
            self._faculty.append(faculty)
            return True
        return False
    
    def get_faculty(self, faculty_id):
        for faculty in self._faculty:
            if faculty.id == faculty_id:
                return faculty
        return None
    
    def get_all_faculty(self):
        return self._faculty.copy()

    # New: Remove faculty and their course assignments
    def remove_faculty(self, faculty_id):
        faculty_to_remove = self.get_faculty(faculty_id)
        if faculty_to_remove:
            # Unassign faculty from all courses they are assigned to
            for course in self._courses:
                if course.assigned_faculty_id == faculty_id:
                    course.assigned_faculty_id = None
                    faculty_to_remove.unassign_course(course.course_code) # Also update faculty's own list
            self._faculty.remove(faculty_to_remove)
            return True
        return False

    def add_course(self, course):
        if not any(c.course_code == course.course_code for c in self._courses):
            self._courses.append(course)
            return True
        return False

    def get_course(self, course_code):
        for course in self._courses:
            if course.course_code == course_code:
                return course
        return None

    def get_all_courses(self):
        return self._courses.copy()

    def enroll_student_in_course(self, student_id, course_code):
        student = self.get_student(student_id)
        course = self.get_course(course_code)
        if student and course:
            if course_code not in student.enrolled_course_codes: # Prevent duplicate enrollment
                student.enroll_course(course_code)
                course.add_student_id(student_id)
                return True # Successfully enrolled
            else:
                return False # Student is already enrolled in this course
        return False # Student or course not found
    
    # New: Drop student from a specific course
    def drop_student_from_course(self, student_id, course_code):
        student = self.get_student(student_id)
        course = self.get_course(course_code)
        if student and course:
            if student_id in course.enrolled_student_ids: # Check if actually enrolled
                student.drop_course(course_code)
                course.remove_student_id(student_id)
                return True # Successfully dropped
            else:
                return False # Student not enrolled in this course
        return False # Student or course not found

    def assign_faculty_to_course(self, faculty_id, course_code):
        faculty = self.get_faculty(faculty_id)
        course = self.get_course(course_code)
        if faculty and course:
            # Check if course is already assigned to this faculty
            if course.assigned_faculty_id == faculty_id:
                return False # Faculty already assigned to this course, no new action needed
            
            # If assigned to a different faculty, unassign them first
            if course.assigned_faculty_id is not None and course.assigned_faculty_id != faculty_id:
                old_faculty = self.get_faculty(course.assigned_faculty_id)
                if old_faculty:
                    old_faculty.unassign_course(course_code) # Update old faculty's list
            
            # Now assign the new faculty
            course.assigned_faculty_id = faculty_id
            faculty.assign_course(course_code)
            return True # Successfully assigned/reassigned
        return False # Faculty or course not found
    
    # New: Unassign faculty from a specific course
    def unassign_faculty_from_course(self, faculty_id, course_code):
        faculty = self.get_faculty(faculty_id)
        course = self.get_course(course_code)
        if faculty and course:
            if course.assigned_faculty_id == faculty_id: # Check if this faculty is assigned to this course
                faculty.unassign_course(course_code)
                course.assigned_faculty_id = None
                return True
            else:
                return False # This faculty is not assigned to this course
        return False

    def get_course_roster(self, course_code):
        course = self.get_course(course_code)
        if course:
            return [self.get_student(student_id) for student_id in course.enrolled_student_ids]
        return []

# ############################################################################
#
# VIEW & CONTROLLER
#
# The class below defines the user interface of the application.
# ############################################################################

class UniversityApp(tk.Tk):
    def __init__(self, university):
        super().__init__()
        self.university = university
        self.title("University Management System")
        
        # Increased overall window size
        self.geometry("1200x800") 
        self.configure(bg='#f0f0f0')

        # Style configuration
        self.style = ttk.Style()
        self.style.theme_use('clam')
        
        # Define larger fonts
        self.large_font = tkFont.Font(family="Arial", size=14)
        self.medium_font = tkFont.Font(family="Arial", size=12)
        self.button_font = tkFont.Font(family="Arial", size=12, weight="bold")
        self.heading_font = tkFont.Font(family="Arial", size=12, weight="bold")

        # Configure colors and fonts for all themed widgets
        self.style.configure('TFrame', background='#f0f0f0')
        self.style.configure('TLabel', background='#f0f0f0', foreground='#333333', font=self.large_font)
        self.style.configure('TEntry', font=self.large_font, padding=5) # Increased padding for entries
        self.style.configure('TButton', background='#4CAF50', foreground='white', font=self.button_font, padding=(10, 5)) # Increased padding for buttons
        self.style.map('TButton', 
                      background=[('active', '#45a049'), ('disabled', '#cccccc')])
        self.style.configure('TLabelFrame', background='#f0f0f0', foreground='#333333', font=self.heading_font)
        
        self.style.configure('Treeview', background='white', foreground='black', fieldbackground='white', font=self.medium_font, rowheight=25) # Increased font and row height
        self.style.map('Treeview', background=[('selected', '#4CAF50')])
        self.style.configure('Treeview.Heading', background='#333333', foreground='white', font=self.heading_font)
        
        self.style.configure('TNotebook', background='#f0f0f0')
        self.style.configure('TNotebook.Tab', background='#dddddd', foreground='#333333', font=self.large_font, padding=(10, 5)) # Increased padding for tabs
        self.style.map('TNotebook.Tab', 
                      background=[('selected', '#4CAF50'), ('active', '#45a049')],
                      foreground=[('selected', 'white'), ('active', 'white')])

        # Create a notebook for tabs
        self.notebook = ttk.Notebook(self)
        # Increased padding around the notebook
        self.notebook.pack(pady=20, padx=20, fill="both", expand=True)

        # Create frames for each tab
        self.students_tab = ttk.Frame(self.notebook)
        self.faculty_tab = ttk.Frame(self.notebook)
        self.courses_tab = ttk.Frame(self.notebook)
        self.enrollment_tab = ttk.Frame(self.notebook)
        self.roster_tab = ttk.Frame(self.notebook)

        self.notebook.add(self.students_tab, text="Students")
        self.notebook.add(self.faculty_tab, text="Faculty")
        self.notebook.add(self.courses_tab, text="Courses")
        self.notebook.add(self.enrollment_tab, text="Enrollment")
        self.notebook.add(self.roster_tab, text="Roster")

        # Populate each tab
        self.create_students_tab()
        self.create_faculty_tab()
        self.create_courses_tab()
        self.create_enrollment_tab()
        self.create_roster_tab()

    def create_students_tab(self):
        # Frame for adding a new student
        add_student_frame = ttk.LabelFrame(self.students_tab, text="Add New Student", padding=(20, 20))
        add_student_frame.pack(fill="x", padx=20, pady=20)

        add_student_frame.columnconfigure(1, weight=1)

        ttk.Label(add_student_frame, text="ID:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.student_id_entry = ttk.Entry(add_student_frame, width=30)
        self.student_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(add_student_frame, text="Name:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.student_name_entry = ttk.Entry(add_student_frame, width=30)
        self.student_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(add_student_frame, text="Major:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.student_major_entry = ttk.Entry(add_student_frame, width=30)
        self.student_major_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        add_student_button = ttk.Button(add_student_frame, text="Add Student", command=self.add_student)
        add_student_button.grid(row=3, column=0, columnspan=2, pady=20)
        
        # New: Frame for removing a student
        remove_student_frame = ttk.LabelFrame(self.students_tab, text="Remove Student", padding=(20, 20))
        remove_student_frame.pack(fill="x", padx=20, pady=10) 

        remove_student_frame.columnconfigure(1, weight=1)

        ttk.Label(remove_student_frame, text="Student ID:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.remove_student_id_entry = ttk.Entry(remove_student_frame, width=30)
        self.remove_student_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        remove_student_button = ttk.Button(remove_student_frame, text="Remove Student", command=self.remove_student_ui)
        remove_student_button.grid(row=1, column=0, columnspan=2, pady=20)

        # Frame for displaying all students
        display_students_frame = ttk.LabelFrame(self.students_tab, text="All Students", padding=(20, 20))
        display_students_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.students_tree = ttk.Treeview(display_students_frame, columns=("ID", "Name", "Major"), show="headings")
        self.students_tree.heading("ID", text="ID")
        self.students_tree.heading("Name", text="Name")
        self.students_tree.heading("Major", text="Major")
        
        self.students_tree.column("ID", width=100, anchor="center")
        self.students_tree.column("Name", width=250, anchor="w")
        self.students_tree.column("Major", width=200, anchor="w")

        self.students_tree.pack(fill="both", expand=True)
        
        self.update_students_list()

    def create_faculty_tab(self):
        # Frame for adding a new faculty member
        add_faculty_frame = ttk.LabelFrame(self.faculty_tab, text="Add New Faculty", padding=(20, 20))
        add_faculty_frame.pack(fill="x", padx=20, pady=20)

        add_faculty_frame.columnconfigure(1, weight=1)

        ttk.Label(add_faculty_frame, text="ID:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.faculty_id_entry = ttk.Entry(add_faculty_frame, width=30)
        self.faculty_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(add_faculty_frame, text="Name:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.faculty_name_entry = ttk.Entry(add_faculty_frame, width=30)
        self.faculty_name_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(add_faculty_frame, text="Department:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.faculty_department_entry = ttk.Entry(add_faculty_frame, width=30)
        self.faculty_department_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        add_faculty_button = ttk.Button(add_faculty_frame, text="Add Faculty", command=self.add_faculty)
        add_faculty_button.grid(row=3, column=0, columnspan=2, pady=20)

        # New: Frame for removing a faculty
        remove_faculty_frame = ttk.LabelFrame(self.faculty_tab, text="Remove Faculty", padding=(20, 20))
        remove_faculty_frame.pack(fill="x", padx=20, pady=10)

        remove_faculty_frame.columnconfigure(1, weight=1)

        ttk.Label(remove_faculty_frame, text="Faculty ID:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.remove_faculty_id_entry = ttk.Entry(remove_faculty_frame, width=30)
        self.remove_faculty_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        remove_faculty_button = ttk.Button(remove_faculty_frame, text="Remove Faculty", command=self.remove_faculty_ui)
        remove_faculty_button.grid(row=1, column=0, columnspan=2, pady=20)

        # Frame for displaying all faculty
        display_faculty_frame = ttk.LabelFrame(self.faculty_tab, text="All Faculty", padding=(20, 20))
        display_faculty_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.faculty_tree = ttk.Treeview(display_faculty_frame, columns=("ID", "Name", "Department"), show="headings")
        self.faculty_tree.heading("ID", text="ID")
        self.faculty_tree.heading("Name", text="Name")
        self.faculty_tree.heading("Department", text="Department")

        self.faculty_tree.column("ID", width=100, anchor="center")
        self.faculty_tree.column("Name", width=250, anchor="w")
        self.faculty_tree.column("Department", width=200, anchor="w")

        self.faculty_tree.pack(fill="both", expand=True)

        self.update_faculty_list()

    def create_courses_tab(self):
        # Frame for adding a new course
        add_course_frame = ttk.LabelFrame(self.courses_tab, text="Add New Course", padding=(20, 20))
        add_course_frame.pack(fill="x", padx=20, pady=20)

        add_course_frame.columnconfigure(1, weight=1)

        ttk.Label(add_course_frame, text="Code:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.course_code_entry = ttk.Entry(add_course_frame, width=30)
        self.course_code_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(add_course_frame, text="Title:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.course_title_entry = ttk.Entry(add_course_frame, width=30)
        self.course_title_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        ttk.Label(add_course_frame, text="Credits:").grid(row=2, column=0, padx=10, pady=10, sticky="w")
        self.course_credits_entry = ttk.Entry(add_course_frame, width=30)
        self.course_credits_entry.grid(row=2, column=1, padx=10, pady=10, sticky="ew")

        add_course_button = ttk.Button(add_course_frame, text="Add Course", command=self.add_course)
        add_course_button.grid(row=3, column=0, columnspan=2, pady=20)

        # Frame for displaying all courses
        display_courses_frame = ttk.LabelFrame(self.courses_tab, text="All Courses", padding=(20, 20))
        display_courses_frame.pack(fill="both", expand=True, padx=20, pady=20)

        self.courses_tree = ttk.Treeview(display_courses_frame, columns=("Code", "Title", "Credits"), show="headings")
        self.courses_tree.heading("Code", text="Code")
        self.courses_tree.heading("Title", text="Title")
        self.courses_tree.heading("Credits", text="Credits")

        self.courses_tree.column("Code", width=120, anchor="center")
        self.courses_tree.column("Title", width=300, anchor="w")
        self.courses_tree.column("Credits", width=80, anchor="center")

        self.courses_tree.pack(fill="both", expand=True)

        self.update_courses_list()

    def create_enrollment_tab(self):
        enrollment_frame = ttk.LabelFrame(self.enrollment_tab, text="Enroll Student in Course", padding=(20, 20))
        enrollment_frame.pack(fill="x", padx=20, pady=20)

        enrollment_frame.columnconfigure(1, weight=1)

        ttk.Label(enrollment_frame, text="Student ID:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.enroll_student_id_entry = ttk.Entry(enrollment_frame, width=30)
        self.enroll_student_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(enrollment_frame, text="Course Code:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.enroll_course_code_entry = ttk.Entry(enrollment_frame, width=30)
        self.enroll_course_code_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        enroll_button = ttk.Button(enrollment_frame, text="Enroll Student", command=self.enroll_student)
        enroll_button.grid(row=2, column=0, columnspan=2, pady=20)
        
        assign_faculty_frame = ttk.LabelFrame(self.enrollment_tab, text="Assign Faculty to Course", padding=(20, 20))
        assign_faculty_frame.pack(fill="x", padx=20, pady=20)
        
        assign_faculty_frame.columnconfigure(1, weight=1)

        ttk.Label(assign_faculty_frame, text="Faculty ID:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.assign_faculty_id_entry = ttk.Entry(assign_faculty_frame, width=30)
        self.assign_faculty_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(assign_faculty_frame, text="Course Code:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.assign_course_code_entry = ttk.Entry(assign_faculty_frame, width=30)
        self.assign_course_code_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")
        
        assign_button = ttk.Button(assign_faculty_frame, text="Assign Faculty", command=self.assign_faculty)
        assign_button.grid(row=2, column=0, columnspan=2, pady=20)

        # New: Frame for dropping student from course
        drop_enrollment_frame = ttk.LabelFrame(self.enrollment_tab, text="Drop Student from Course", padding=(20, 20))
        drop_enrollment_frame.pack(fill="x", padx=20, pady=20)

        drop_enrollment_frame.columnconfigure(1, weight=1)

        ttk.Label(drop_enrollment_frame, text="Student ID:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.drop_enroll_student_id_entry = ttk.Entry(drop_enrollment_frame, width=30)
        self.drop_enroll_student_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(drop_enrollment_frame, text="Course Code:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.drop_enroll_course_code_entry = ttk.Entry(drop_enrollment_frame, width=30)
        self.drop_enroll_course_code_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        drop_enroll_button = ttk.Button(drop_enrollment_frame, text="Drop Enrollment", command=self.drop_enrollment_ui)
        drop_enroll_button.grid(row=2, column=0, columnspan=2, pady=20)

        # New: Frame for unassigning faculty from course
        unassign_faculty_frame = ttk.LabelFrame(self.enrollment_tab, text="Unassign Faculty from Course", padding=(20, 20))
        unassign_faculty_frame.pack(fill="x", padx=20, pady=20)
        
        unassign_faculty_frame.columnconfigure(1, weight=1)

        ttk.Label(unassign_faculty_frame, text="Faculty ID:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.unassign_faculty_id_entry = ttk.Entry(unassign_faculty_frame, width=30)
        self.unassign_faculty_id_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        ttk.Label(unassign_faculty_frame, text="Course Code:").grid(row=1, column=0, padx=10, pady=10, sticky="w")
        self.unassign_course_code_entry = ttk.Entry(unassign_faculty_frame, width=30)
        self.unassign_course_code_entry.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        unassign_button = ttk.Button(unassign_faculty_frame, text="Unassign Faculty", command=self.unassign_faculty_ui)
        unassign_button.grid(row=2, column=0, columnspan=2, pady=20)


    def create_roster_tab(self):
        roster_frame = ttk.LabelFrame(self.roster_tab, text="View Course Roster", padding=(20, 20))
        roster_frame.pack(fill="x", padx=20, pady=20)

        roster_frame.columnconfigure(1, weight=1)

        ttk.Label(roster_frame, text="Course Code:").grid(row=0, column=0, padx=10, pady=10, sticky="w")
        self.roster_course_code_entry = ttk.Entry(roster_frame, width=30)
        self.roster_course_code_entry.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        view_roster_button = ttk.Button(roster_frame, text="View Roster", command=self.view_roster)
        view_roster_button.grid(row=1, column=0, columnspan=2, pady=20)
        
        self.roster_tree = ttk.Treeview(self.roster_tab, columns=("ID", "Name", "Major"), show="headings")
        self.roster_tree.heading("ID", text="ID")
        self.roster_tree.heading("Name", text="Name")
        self.roster_tree.heading("Major", text="Major")

        self.roster_tree.column("ID", width=100, anchor="center")
        self.roster_tree.column("Name", width=250, anchor="w")
        self.roster_tree.column("Major", width=200, anchor="w")
        
        self.roster_tree.pack(fill="both", expand=True, padx=20, pady=20)

    def add_student(self):
        id = self.student_id_entry.get().strip()
        name = self.student_name_entry.get().strip()
        major = self.student_major_entry.get().strip()
        if id and name and major:
            student = Student(id, name, major)
            if self.university.add_student(student):
                self.update_students_list()
                self.student_id_entry.delete(0, tk.END)
                self.student_name_entry.delete(0, tk.END)
                self.student_major_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Student added successfully!")
            else:
                messagebox.showerror("Error", "Student with this ID already exists.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    # New: UI method to remove a student
    def remove_student_ui(self):
        student_id = self.remove_student_id_entry.get().strip()
        if student_id:
            if self.university.remove_student(student_id):
                messagebox.showinfo("Success", f"Student {student_id} removed successfully!")
                self.update_students_list()
                self.remove_student_id_entry.delete(0, tk.END)
                # Refresh courses list as student enrollments are removed
                self.update_courses_list() # Not strictly necessary for how courses are displayed, but good for consistency
            else:
                messagebox.showerror("Error", f"Student with ID '{student_id}' not found.")
        else:
            messagebox.showerror("Error", "Please enter a Student ID to remove.")

    def add_faculty(self):
        id = self.faculty_id_entry.get().strip()
        name = self.faculty_name_entry.get().strip()
        department = self.faculty_department_entry.get().strip()
        if id and name and department:
            faculty = Faculty(id, name, department)
            if self.university.add_faculty(faculty):
                self.update_faculty_list()
                self.faculty_id_entry.delete(0, tk.END)
                self.faculty_name_entry.delete(0, tk.END)
                self.faculty_department_entry.delete(0, tk.END)
                messagebox.showinfo("Success", "Faculty added successfully!")
            else:
                messagebox.showerror("Error", "Faculty with this ID already exists.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    # New: UI method to remove a faculty
    def remove_faculty_ui(self):
        faculty_id = self.remove_faculty_id_entry.get().strip()
        if faculty_id:
            if self.university.remove_faculty(faculty_id):
                messagebox.showinfo("Success", f"Faculty {faculty_id} removed successfully!")
                self.update_faculty_list()
                self.remove_faculty_id_entry.delete(0, tk.END)
                # Refresh courses list as faculty assignments are removed
                self.update_courses_list() # Not strictly necessary for how courses are displayed, but good for consistency
            else:
                messagebox.showerror("Error", f"Faculty with ID '{faculty_id}' not found.")
        else:
            messagebox.showerror("Error", "Please enter a Faculty ID to remove.")


    def add_course(self):
        code = self.course_code_entry.get().strip()
        title = self.course_title_entry.get().strip()
        credits_str = self.course_credits_entry.get().strip()
        if code and title and credits_str:
            try:
                credits = float(credits_str) # Ensure credits is a number
                course = Course(code, title, credits)
                if self.university.add_course(course):
                    self.update_courses_list()
                    self.course_code_entry.delete(0, tk.END)
                    self.course_title_entry.delete(0, tk.END)
                    self.course_credits_entry.delete(0, tk.END)
                    messagebox.showinfo("Success", "Course added successfully!")
                else:
                    messagebox.showerror("Error", "Course with this code already exists.")
            except ValueError:
                messagebox.showerror("Error", "Credits must be a number.")
        else:
            messagebox.showerror("Error", "Please fill in all fields.")

    def enroll_student(self):
        student_id = self.enroll_student_id_entry.get().strip()
        course_code = self.enroll_course_code_entry.get().strip()
        if student_id and course_code:
            student_exists = self.university.get_student(student_id)
            course_exists = self.university.get_course(course_code)
            
            if not student_exists:
                messagebox.showerror("Error", f"Student with ID '{student_id}' does not exist.")
                return
            if not course_exists:
                messagebox.showerror("Error", f"Course with code '{course_code}' does not exist.")
                return
            
            if self.university.enroll_student_in_course(student_id, course_code):
                messagebox.showinfo("Success", f"Student {student_id} enrolled in {course_code} successfully!")
                self.enroll_student_id_entry.delete(0, tk.END)
                self.enroll_course_code_entry.delete(0, tk.END)
            else: # This branch is hit if the student is already enrolled
                messagebox.showinfo("Info", "Student is already enrolled in this course.")
        else:
            messagebox.showerror("Error", "Please provide both student ID and course code.")
            
    # New: UI method to drop student from a course
    def drop_enrollment_ui(self):
        student_id = self.drop_enroll_student_id_entry.get().strip()
        course_code = self.drop_enroll_course_code_entry.get().strip()
        if student_id and course_code:
            student_exists = self.university.get_student(student_id)
            course_exists = self.university.get_course(course_code)

            if not student_exists:
                messagebox.showerror("Error", f"Student with ID '{student_id}' does not exist.")
                return
            if not course_exists:
                messagebox.showerror("Error", f"Course with code '{course_code}' does not exist.")
                return

            if self.university.drop_student_from_course(student_id, course_code):
                messagebox.showinfo("Success", f"Student {student_id} dropped from {course_code} successfully!")
                self.drop_enroll_student_id_entry.delete(0, tk.END)
                self.drop_enroll_course_code_entry.delete(0, tk.END)
            else:
                messagebox.showerror("Error", f"Student {student_id} is not enrolled in {course_code}.")
        else:
            messagebox.showerror("Error", "Please provide both student ID and course code.")


    def assign_faculty(self):
        faculty_id = self.assign_faculty_id_entry.get().strip()
        course_code = self.assign_course_code_entry.get().strip()
        if faculty_id and course_code:
            faculty_exists = self.university.get_faculty(faculty_id)
            course_exists = self.university.get_course(course_code)

            if not faculty_exists:
                messagebox.showerror("Error", f"Faculty with ID '{faculty_id}' does not exist.")
                return
            if not course_exists:
                messagebox.showerror("Error", f"Course with code '{course_code}' does not exist.")
                return

            # Check if assignment actually changes anything
            current_course = self.university.get_course(course_code)
            if current_course.assigned_faculty_id == faculty_id:
                messagebox.showinfo("Info", "Faculty is already assigned to this course.")
                return # Exit early if no change is needed

            if self.university.assign_faculty_to_course(faculty_id, course_code):
                # If course was previously assigned to someone else, inform the user
                # We can't easily tell *here* if it was a re-assignment or a new assignment
                # without more state from the model's assign_faculty_to_course method.
                # However, the current model removes the "old_faculty" if different,
                # ensuring the state is correct.
                messagebox.showinfo("Success", f"Faculty {faculty_id} assigned to {course_code} successfully!")
                self.assign_faculty_id_entry.delete(0, tk.END)
                self.assign_course_code_entry.delete(0, tk.END)
                self.update_courses_list() # Courses list is updated to reflect faculty assignment if displayed
            # No `else` needed here because if assign_faculty_to_course returns False,
            # it means the faculty or course didn't exist (handled above) or the faculty
            # was already assigned (handled by the prior `if current_course.assigned_faculty_id == faculty_id` check).
            # If the model had a reason to return False for a valid faculty/course and it wasn't a duplicate assignment,
            # we would add an error message here.
        else:
            messagebox.showerror("Error", "Please provide both faculty ID and course code.")
    
    # New: UI method to unassign faculty from a course
    def unassign_faculty_ui(self):
        faculty_id = self.unassign_faculty_id_entry.get().strip()
        course_code = self.unassign_course_code_entry.get().strip()
        if faculty_id and course_code:
            faculty_exists = self.university.get_faculty(faculty_id)
            course_exists = self.university.get_course(course_code)

            if not faculty_exists:
                messagebox.showerror("Error", f"Faculty with ID '{faculty_id}' does not exist.")
                return
            if not course_exists:
                messagebox.showerror("Error", f"Course with code '{course_code}' does not exist.")
                return

            if self.university.unassign_faculty_from_course(faculty_id, course_code):
                messagebox.showinfo("Success", f"Faculty {faculty_id} unassigned from {course_code} successfully!")
                self.unassign_faculty_id_entry.delete(0, tk.END)
                self.unassign_course_code_entry.delete(0, tk.END)
                self.update_courses_list() # Update courses list to reflect faculty assignment change
            else:
                messagebox.showerror("Error", f"Faculty {faculty_id} is not assigned to {course_code}, or course {course_code} has no faculty assigned.")
        else:
            messagebox.showerror("Error", "Please provide both faculty ID and course code.")


    def update_students_list(self):
        for i in self.students_tree.get_children():
            self.students_tree.delete(i)
        for student in self.university.get_all_students():
            self.students_tree.insert("", "end", values=(student.id, student.name, student.major))

    def update_faculty_list(self):
        for i in self.faculty_tree.get_children():
            self.faculty_tree.delete(i)
        for faculty in self.university.get_all_faculty():
            self.faculty_tree.insert("", "end", values=(faculty.id, faculty.name, faculty.department))

    def update_courses_list(self):
        for i in self.courses_tree.get_children():
            self.courses_tree.delete(i)
        for course in self.university.get_all_courses():
            # The original treeview only shows Code, Title, Credits.
            # If we wanted to show assigned faculty, a column would need to be added.
            # The internal model is correctly updated even if not visibly reflected here.
            self.courses_tree.insert("", "end", values=(course.course_code, course.title, course.credits))


    def view_roster(self):
        course_code = self.roster_course_code_entry.get().strip()
        if course_code:
            course = self.university.get_course(course_code)
            if not course:
                messagebox.showerror("Error", f"Course with code '{course_code}' does not exist.")
                for i in self.roster_tree.get_children(): # Clear previous roster
                    self.roster_tree.delete(i)
                return

            roster = self.university.get_course_roster(course_code)
            for i in self.roster_tree.get_children():
                self.roster_tree.delete(i)
            if roster:
                for student in roster:
                    self.roster_tree.insert("", "end", values=(student.id, student.name, student.major))
            else:
                messagebox.showinfo("Info", f"No students enrolled in course '{course_code}'.")
        else:
            messagebox.showerror("Error", "Please provide a course code.")


if __name__ == "__main__":
    university = University()
    
    # Add some initial dummy data for testing the UI
    university.add_student(Student("S001", "Alice Smith", "Computer Science"))
    university.add_student(Student("S002", "Bob Johnson", "Mathematics"))
    university.add_faculty(Faculty("F001", "Dr. Carol White", "Computer Science"))
    university.add_faculty(Faculty("F002", "Prof. David Green", "Physics"))
    university.add_course(Course("CS101", "Intro to Programming", 3))
    university.add_course(Course("MA201", "Calculus I", 4))
    university.enroll_student_in_course("S001", "CS101")
    university.enroll_student_in_course("S002", "MA201")
    university.assign_faculty_to_course("F001", "CS101")
    university.add_course(Course("PH101", "Intro to Physics", 3)) # Add another course
    university.assign_faculty_to_course("F002", "PH101") # Assign faculty to it

    app = UniversityApp(university)
    app.mainloop()
