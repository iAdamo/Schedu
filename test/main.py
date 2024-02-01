#!/usr/bin/python3
from models import storage
from models import guardian
from models.admin import Admin
from models.teacher import Teacher
from models.student import Student
from models.guardian import Guardian


def id_generator(first_name, cls, num):
    """generates school ids
    """
    sch = "schedu"
    return f"{sch}-{cls.__name__}-{first_name[:3]}-{str(num).zfill(4)}".lower()


def get_user_by_nin(nin):
    all_objs = storage.all()
    for obj in all_objs.values():
        if isinstance(obj, (Teacher, Student)) and obj.nin == nin:
            return obj
    return None

print("-- Create a new Admin --")
admin = Admin()
admin.first_name = "Alice"
admin.last_name = "Smith"
admin.email = "admin@mail.com"
admin.password = "admin"
admin.id = id_generator(
    admin.first_name, Admin, len(
        storage.all(Admin)))
admin.save()
print(admin)

print("-- Create a new Teacher --")
teacher = Teacher()
teacher.nin = "1234"
if not get_user_by_nin(teacher.nin):
    teacher.first_name = "Betty"
    teacher.last_name = "Bar"
    teacher.email = "airbnb@mail.com"
    teacher.password = "root"
    teacher.id = id_generator(
        teacher.first_name, Teacher, len(
            storage.all(Teacher)))
    teacher.save()
    print(teacher)

print("-- Create a new Student --")
student = Student()
student.nin = "5656"
if not get_user_by_nin(student.nin):
    student.first_name = "John"
    student.email = "airbnb2@mail.com"
    student.password = "root"
    student.guardian_first_name = "Big"
    student.guardian_last_name = "Fat"
    student.id = id_generator(
    student.first_name, Student, len(
            storage.all(Student)))
    student.save()
    print(student)

    print("-- Create a new Guardian --")
    guardian = Guardian()
    guardian.first_name = student.guardian_first_name
    guardian.last_name = student.guardian_last_name
    guardian.email = "airbnb2@mail.com"
    guardian.password = "root"
    guardian.id = id_generator(
        guardian.first_name, Guardian, len(
            storage.all(Guardian)))
    guardian.save()
    print(guardian)
