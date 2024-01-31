import uuid
from datetime import datetime

class BaseModel:
    """Defines the base model for other classes"""

    def __init__(self, *args, **kwargs):
        """Initialize the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key == 'created_at' or key == 'updated_at':
                    value = datetime.strptime(value, "%Y-%m-%dT%H:%M:%S.%f")
                if key != '__class__':
                    setattr(self, key, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()

    def __str__(self):
        """Return string representation of BaseModel"""
        cls_name = self.__class__.__name__
        return "[{}] ({}) {}".format(cls_name, self.id, self.__dict__)

    def save(self):
        """Update updated_at with current datetime and save to storage"""
        self.updated_at = datetime.now()
        from models import storage
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Return a dictionary representation of BaseModel"""
        new_dict = self.__dict__.copy()
        new_dict['__class__'] = self.__class__.__name__
        new_dict['created_at'] = self.created_at.isoformat()
        new_dict['updated_at'] = self.updated_at.isoformat()
        return new_dict

    def delete(self):
        """Delete the current instance from storage"""
        from models import storage
        storage.delete(self)

    @classmethod
    def all(cls):
        """Return a dictionary of all instances of the class"""
        from models import storage
        return storage.all(cls)

    @classmethod
    def count(cls):
        """Count the number of instances of the class"""
        from models import storage
        return storage.count(cls)

    @classmethod
    def get(cls, id):
        """Get an instance of the class by its ID"""
        from models import storage
        return storage.get(cls, id)

    def update(self, **kwargs):
        """Update attributes of the instance"""
        for key, value in kwargs.items():
            if key != 'id' and key != 'created_at' and key != 'updated_at':
                setattr(self, key, value)
        self.save()