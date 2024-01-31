import json
from models.base_model import BaseModel

class FileStorage:
    """Serializes instances to a JSON file & deserializes back to instances"""

    __file_path = "file.json"
    __objects = {}

    def all(self, cls=None):
        """Returns the dictionary __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f, indent=2)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                class_name, obj_id = key.split('.')
                if class_name in self.classes:
                    self.__objects[key] = self.classes[class_name](**jo[key])
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """Delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def get(self, cls, id):
        """Retrieve one object"""
        if cls is not None and id is not None:
            key = cls.__name__ + '.' + id
            if key in self.__objects:
                return self.__objects[key]
        return None

    def count(self, cls=None):
        """Count the number of objects in storage"""
        if cls is not None:
            return len(self.all(cls))
        return len(self.__objects)

    def close(self):
        """Call reload() method for deserializing the JSON file to objects"""
        self.reload()