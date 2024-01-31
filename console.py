import cmd
from models.teacher import Teacher
from models.student import Student
from models.guardian import Guardian
from models.engines.db_storage import DBStorage
from models.engines.file_storage import FileStorage


class SchoolManagementConsole(cmd.Cmd):
    prompt = '(school_mgmt) '

    def __init__(self, storage_type='db'):
        super().__init__()
        self.storage_type = storage_type
        if self.storage_type == 'db':
            self.storage = DBStorage()
        elif self.storage_type == 'file':
            self.storage = FileStorage()
            self.storage.reload()
        else:
            raise ValueError("Invalid storage type. Choose 'db' or 'file'.")
        self.session = None  # No session attribute in DBStorage

    def do_EOF(self, arg):
        return True

    def emptyline(self):
        pass

    def do_quit(self, arg):
        return True

    def register_admin(self, username, password):
        """Register a new admin."""
        admin = Admin(username=username, password=password)
        self.storage.new(admin)
        self.storage.save()
        print("Admin registered successfully.")

    def register_teacher(self, name, gender, dob, discipline, classroom, phone_number, address, email):
        """Register a new teacher."""
        teacher = Teacher(name=name, gender=gender, dob=dob, discipline=discipline,
                          classroom=classroom, phone_number=phone_number, address=address, email=email)
        self.storage.new(teacher)
        self.storage.save()
        print("Teacher registered successfully.")

    def register_student(self, name, gender, dob, class_name, height, genotype_blood_group, parent_guardian_id):
        """Register a new student."""
        student = Student(name=name, gender=gender, dob=dob, class_name=class_name,
                          height=height, genotype_blood_group=genotype_blood_group, parent_guardian_id=parent_guardian_id)
        self.storage.new(student)
        self.storage.save()
        print("Student registered successfully.")

    def register_guardian(self, name, gender, dob, occupation, child_name, address, phone, email):
        """Register a new guardian."""
        guardian = Guardian(name=name, gender=gender, dob=dob, occupation=occupation,
                            child_name=child_name, address=address, phone=phone, email=email)
        self.storage.new(guardian)
        self.storage.save()
        print("Guardian registered successfully.")

    def show_admins(self):
        """Show all registered admins."""
        admins = self.storage.all(Admin)
        for admin in admins.values():
            print(admin)

    def show_teachers(self):
        """Show all registered teachers."""
        teachers = self.storage.all(Teacher)
        for teacher in teachers.values():
            print(teacher)

    def show_students(self):
        """Show all registered students."""
        students = self.storage.all(Student)
        for student in students.values():
            print(student)

    def show_guardians(self):
        """Show all registered guardians."""
        guardians = self.storage.all(Guardian)
        for guardian in guardians.values():
            print(guardian)

    def update_admin(self, admin_id, new_password):
        """Update admin password."""
        admin = self.storage.get(Admin, admin_id)
        if admin:
            admin.password = new_password
            self.storage.save()
            print("Admin password updated successfully.")
        else:
            print("Admin not found.")

    def update_teacher(self, teacher_id, attribute, new_value):
        """Update teacher information."""
        teacher = self.storage.get(Teacher, teacher_id)
        if teacher:
            setattr(teacher, attribute, new_value)
            self.storage.save()
            print("Teacher information updated successfully.")
        else:
            print("Teacher not found.")

    def update_student(self, student_id, attribute, new_value):
        """Update student information."""
        student = self.storage.get(Student, student_id)
        if student:
            setattr(student, attribute, new_value)
            self.storage.save()
            print("Student information updated successfully.")
        else:
            print("Student not found.")

    def update_guardian(self, guardian_id, attribute, new_value):
        """Update guardian information."""
        guardian = self.storage.get(Guardian, guardian_id)
        if guardian:
            setattr(guardian, attribute, new_value)
            self.storage.save()
            print("Guardian information updated successfully.")
        else:
            print("Guardian not found.")

    def delete_admin(self, admin_id):
        """Delete admin."""
        admin = self.storage.get(Admin, admin_id)
        if admin:
            self.storage.delete(admin)
            self.storage.save()
            print("Admin deleted successfully.")
        else:
            print("Admin not found.")

    def delete_teacher(self, teacher_id):
        """Delete teacher."""
        teacher = self.storage.get(Teacher, teacher_id)
        if teacher:
            self.storage.delete(teacher)
            self.storage.save()
            print("Teacher deleted successfully.")
        else:
            print("Teacher not found.")

    def delete_student(self, student_id):
        """Delete student."""
        student = self.storage.get(Student, student_id)
        if student:
            self.storage.delete(student)
            self.storage.save()
            print("Student deleted successfully.")
        else:
            print("Student not found.")

    def delete_guardian(self, guardian_id):
        """Delete guardian."""
        guardian = self.storage.get(Guardian, guardian_id)
        if guardian:
            self.storage.delete(guardian)
            self.storage.save()
            print("Guardian deleted successfully.")
        else:
            print("Guardian not found.")

    def close(self):
        """Close the console"""
        self.storage.close()
        print("Goodbye!")
        return True

    def default(self, line):
        print("Invalid command. Here's what you can do:")
        print("- To register a new admin, use: register_admin <username> <password>")
        print("- To register a new teacher, use: register_teacher <name> <gender> <dob> <discipline> <classroom> <phone_number> <address> <email>")
        print("- To register a new student, use: register_student <name> <gender> <dob> <class_name> <height> <genotype_blood_group> <parent_guardian_id>")
        print("- To register a new guardian, use: register_guardian <name> <gender> <dob> <occupation> <child_name> <address> <phone> <email>")
        print("- To show all admins, use: show_admins")
        print("- To show all teachers, use: show_teachers")
        print("- To show all students, use: show_students")
        print("- To show all guardians, use: show_guardians")
        print("- To update an admin's password, use: update_admin <admin_id> <new_password>")
        print("- To update a teacher's information, use: update_teacher <teacher_id> <attribute> <new_value>")
        print("- To update a student's information, use: update_student <student_id> <attribute> <new_value>")
        print("- To update a guardian's information, use: update_guardian <guardian_id> <attribute> <new_value>")
        print("- To delete an admin, use: delete_admin <admin_id>")
        print("- To delete a teacher, use: delete_teacher <teacher_id>")
        print("- To delete a student, use: delete_student <student_id>")
        print("- To delete a guardian, use: delete_guardian <guardian_id>")
        print("- Type 'help' for a list of commands")

if __name__ == '__main__':
    SchoolManagementConsole().cmdloop()