#!/usr/bin/python3
"""
Contains class BaseModel for the School Management System
"""

from datetime import datetime
import models
from os import getenv
from sqlalchemy import Column, String, DateTime
from sqlalchemy.ext.declarative import declarative_base
import uuid

time = "%Y-%m-%dT%H:%M:%S.%f"

if models.storage_type == "db":
    Base = declarative_base()
else:
    Base = object


class BaseModel:
    """The BaseModel class from which future classes will be derived"""
    if models.storage_type == "db":
        id = Column(String(60), primary_key=True)
        registered_at = Column(DateTime, default=datetime.utcnow)
        updated_at = Column(DateTime, default=datetime.utcnow)

    def __init__(self, *args, **kwargs):
        """Initialization of the base model"""
        if kwargs:
            for key, value in kwargs.items():
                if key != "__class__":
                    setattr(self, key, value)
            if kwargs.get(
                    "registered_at",
                    None) and isinstance(
                    self.registered_at,
                    str):
                self.registered_at = datetime.strptime(kwargs["registered_at"], time)
            else:
                self.registered_at = datetime.utcnow()
            if kwargs.get(
                    "updated_at",
                    None) and isinstance(
                    self.updated_at,
                    str):
                self.updated_at = datetime.strptime(kwargs["updated_at"], time)
            else:
                self.updated_at = datetime.utcnow()
            if kwargs.get("id", None) is None:
                self.id = ""
        else:
            self.id = ""
            self.registered_at = datetime.utcnow()
            self.updated_at = self.registered_at

    def __str__(self):
        """String representation of the BaseModel class"""
        return "[{:s}] ({:s}) {}".format(self.__class__.__name__, self.id,
                                         self.__dict__)

    def save(self):
        """updates the attribute 'updated_at' with the current datetime"""
        self.updated_at = datetime.utcnow()
        models.storage.new(self)
        models.storage.save()

    def to_dict(self):
        """returns a dictionary containing all keys/values of the instance"""
        new_dict = self.__dict__.copy()
        if "registered_at" in new_dict:
            new_dict["registered_at"] = new_dict["registered_at"].strftime(time)
        if "updated_at" in new_dict:
            new_dict["updated_at"] = new_dict["updated_at"].strftime(time)
        new_dict["__class__"] = self.__class__.__name__
        if "_sa_instance_state" in new_dict:
            del new_dict["_sa_instance_state"]
        if getenv("MGT_TYPE_STORAGE") == "db":
            if "password" in new_dict:
                del new_dict["password"]
        return new_dict

    def delete(self):
        """delete the current instance from the storage"""
        models.storage.delete(self)
