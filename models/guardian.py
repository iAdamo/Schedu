#!/usr/bin/python3
"""holds class Guardian
"""
import models
from models.base_model import BaseModel, Base
from models.student import Student
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Guardian(BaseModel, Base):
    """Representation of guardian """
    if models.storage_type == "db":
        __tablename__ = 'guardians'
        id = Column(String(60), nullable=False, primary_key=True)
        name = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        student_id = Column(
            String(60),
            ForeignKey('students.id'),
            nullable=False)
        student = relationship("Student", backref="guardian")
    else:
        id = ""
        name = ""
        email = ""
        student_id = ""

    def __init__(self, *args, **kwargs):
        """initializes guardian"""
        super().__init__(*args, **kwargs)
        first_name = kwargs.get("first_name", "")
        from models import storage
        count = len(storage.all("Guardian"))
        self.id = f"schedu-guardian-{first_name[:3]}-{str(count).zfill(4)}".lower()
        