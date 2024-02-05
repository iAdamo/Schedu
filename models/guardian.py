#!/usr/bin/python3
""" Holds class Guardian """

import models
from models.base_model import BaseModel, Base
from models.student import Student
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin  # Assuming UserMixin is required for authentication

class Guardian(UserMixin, BaseModel, Base):
    """ Representation of guardian """
    if models.storage_type == "db":
        __tablename__ = 'guardians'
        id = Column(String(60), nullable=False, primary_key=True)
        name = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False, unique=True)
        student_id = Column(String(60), ForeignKey('students.id'), nullable=False)
        student = relationship("Student", backref="guardian")
    else:
        id = ""
        name = ""
        email = ""
        student_id = ""

    def __init__(self, *args, **kwargs):
        """ Initializes guardian """
        super().__init__(*args, **kwargs)
        first_name = kwargs.get("first_name", "")
        from models import storage
        count = len(storage.all("Guardian"))
        self.id = f"schedu-guardian-{first_name[:3]}-{count:04}".lower()

    def is_active(self):
        """ Return True if the user account is active, and False otherwise """
        return True
