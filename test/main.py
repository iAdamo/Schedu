#!/usr/bin/python3
from models import storage
from models.teacher import Teacher
from models.student import Student


all_objs = storage.all()
print("-- Reloaded objects --")
for obj_id in all_objs.keys():
    obj = all_objs[obj_id]
    print(obj)

print("-- Create a new Teacher --")
teacher = Teacher()
teacher.first_name = "Betty"
teacher.last_name = "Bar"
teacher.email = "airbnb@mail.com"
teacher.password = "root"
teacher.save()
print(teacher)

print("-- Create a new Student --")
student = Student()
student.first_name = "John"
student.email = "airbnb2@mail.com"
student.password = "root"
student.genotype_blood_group = ""
student.save()
print(student)
