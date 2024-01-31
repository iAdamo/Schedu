#!/usr/bin/python3
"""holds class Student
"""
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Student(BaseModel, Base):
    """Representation of student """
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

    def __init__(self, *args, **kwargs):
        """initializes student"""
        super().__init__(*args, **kwargs)
