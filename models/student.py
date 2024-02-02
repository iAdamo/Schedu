#!/usr/bin/python3
"""holds class Student
"""
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Student(BaseModel, Base):
    """Representation of student
    """
    count = 0
    
    if models.storage_type == "db":
        __tablename__ = 'students'
        id = Column(String(60), nullable=False, primary_key=True)
        name = Column(String(128), nullable=False)
        grade = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
    else:
        id = ""
        name = ""
        grade = ""
        email = ""
        nin = ""
        phone_number = ""

    def __init__(self, *args, **kwargs):
        """initializes student
        """
        super().__init__(*args, **kwargs)
        first_name = kwargs.get("first_name", "")
        from models import storage
        count = len(storage.all("Student"))
        self.id = f"schedu-student-{first_name[:3]}-{str(count).zfill(4)}".lower()
