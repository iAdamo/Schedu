#!/usr/bin/python3
"""Contains the FileStorage class
"""

import json
from models.base_model import BaseModel
from models.admin import Admin
from models.teacher import Teacher
from models.student import Student
from models.guardian import Guardian

classes = {
    "BaseModel": BaseModel,
    "Teacher": Teacher,
    "Student": Student,
    "Guardian": Guardian,
    "Admin": Admin}


class FileStorage:
    """serializes instances to a JSON file & deserializes back to instances"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def all(self, cls=None):
        """returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f, indent=2)

    def reload(self):
        """deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except BaseException:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it's inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def get(self, cls, id):
        """retrieve one object if class and id are given, or all objects of a
        class if only class is given, or all objects if none are given.
        """
        if cls and id:
            if isinstance(cls, str):
                obj_id = cls + '.' + id
            else:
                obj_id = cls.__name__ + '.' + id
            return self.__objects.get(obj_id)
        elif cls is None and id:
            for obj in self.__objects.values():
                if obj.id == id:
                    return obj
        elif cls and id is None:
            return [obj for obj in self.__objects.values() if obj.__class__ == cls]
        else:
            return None

    def count(self, cls=None):
        """count the number of objects in storage"""
        if cls is not None:
            return len(self.all(cls))
        return len(self.all())

    
    def find(self, string):
        """find and check for first occurrence of string"""
        for obj in self.__objects.values():
            if string in obj.__dict__.values():
                return string
        return None

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
