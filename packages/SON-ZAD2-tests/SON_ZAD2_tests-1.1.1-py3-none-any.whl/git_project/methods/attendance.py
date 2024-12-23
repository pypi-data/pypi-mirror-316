from git_project.methods.import_students import ImportStudents

import os


"""
Module for managing student attendance.
"""

class Attendance:
    def __init__(self):
        self.presence = {}

    # Iterating through the list of students to check attendance
    def check_attendance_for_all(self, date, students):
        if date not in self.presence:
            self.presence[date] = {}

        for student in students:
            student_name = f"{student['Name']} {student['Surname']}"
            present = input(f"Is {student_name} present? (1/0): ") == "1"
            self.presence[date][student_name] = present
            print(
                f"Attendance for student {student_name} on {date} has been updated to {'present' if present else 'absent'}.\n"
            )

    # Displays the attendance list for students
    def download_attendance(self, date):
        if date not in self.presence:
            print(f"No attendance data for {date}.")
            return
        print(f"Attendance for {date}:")
        for student, present in self.presence[date].items():
            print(f"{student}: {'present' if present else 'absent'}")

    # Clearing attendance data
    def clear_attendance(self, date):
        if date in self.presence:
            del self.presence[date]
            print(f"Attendance data for {date} has been removed.")
        else:
            print(f"No attendance data for {date}.")

    # Modifies the attendance of students for a specific date
    def modify_attendance(self, date, student_name):
        if date not in self.presence or student_name not in self.presence[date]:
            print(f"No attendance data found for {student_name} on {date}.")
            return
        present = input(f"Is {student_name} present? (1/0): ") == "1"
        self.presence[date][student_name] = present
        print(
            f"Attendance for student {student_name} on {date} has been updated to {'present' if present else 'absent'}."
        )


if __name__ == "__main__":
    attendance = Attendance()
    students = []

    # Main project directory path
    base_dir = os.path.dirname(os.path.abspath(__file__))

    # Dynamic paths
    file_path_csv = os.path.join(base_dir, "lists", "student_list.csv")
    file_path_txt = os.path.join(base_dir, "lists", "student_list.txt")

    # Checking if the file exists
    try:
        with open(file_path_csv, "r"):
            students = ImportStudents.csv(file_path_csv, ["Name", "Surname", "ID"])
    except FileNotFoundError:

        try:
            with open(file_path_txt, "r"):
                students = ImportStudents.txt(file_path_txt, ["Name", "Surname", "ID"])
        except FileNotFoundError:
            print("No file with the student list found.")

    while True:
        print(
            "\n1. Check Attendance for All\n2. Download Attendance\n3. Modify Attendance\n4. Clear Attendance\n5. Exit"
        )
        choice = input("Choose an option: ")

        if choice == "1":
            date = input("Enter date (YYYY-MM-DD): \n")
            attendance.check_attendance_for_all(date, students)
        elif choice == "2":
            date = input("Enter date (YYYY-MM-DD): \n")
            attendance.download_attendance(date)
        elif choice == "3":
            date = input("Enter date (YYYY-MM-DD): \n")
            student_name = input("Student's full name: (Name Surname): ")
            attendance.modify_attendance(date, student_name)
        elif choice == "4":
            date = input("Enter date (YYYY-MM-DD) to clear attendance: \n")
            attendance.clear_attendance(date)
        elif choice == "5":
            break
        else:
            print("Please try again.\n")
