#!/usr/bin/python3
""" Holds class Student """

import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
# Assuming UserMixin is required for authentication
from flask_login import UserMixin


class Student(UserMixin, BaseModel, Base):
    """Representation of student
    """

    if models.storage_type == "db":
        __tablename__ = 'students'
        id = Column(String(60), nullable=False, primary_key=True)
        name = Column(String(128), nullable=False)
        grade = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False, unique=True)
        guardian_id = Column(String(60), ForeignKey('guardians.id'))
        guardian_relation = relationship("Guardian", backref="students", foreign_keys=[guardian_id])
    else:
        id = ""
        name = ""
        grade = ""
        email = ""
        nin = ""
        phone_number = ""

    def __init__(self, *args, **kwargs):
        """ Initializes student """
        super().__init__(*args, **kwargs)
        first_name = kwargs.get("first_name", "")
        from models import storage
        count = len(storage.all("Student"))
        self.id = f"schedu-student-{first_name[:3]}-{count:04}".lower()

    def is_active(self):
        """Return True if the user account is active, and False otherwise
        """
        if self.active:
            return True
        return False
