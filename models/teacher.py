#!/usr/bin/python3
"""Holds class Teacher
"""

import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class Teacher(UserMixin, BaseModel, Base):
    """Representation of teacher
    """
    if models.storage_type == "db":
        __tablename__ = 'teachers'
        id = Column(String(60), nullable=False, primary_key=True)
        name = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False, unique=True)
        subject = Column(String(128), nullable=False)
    else:
        id = ""
        name = ""
        email = ""
        subject = ""

    def __init__(self, *args, **kwargs):
        """Initializes teacher
        """
        super().__init__(*args, **kwargs)
        first_name = kwargs.get("first_name", "")
        from models import storage
        count = len(storage.all("Teacher"))
        self.id = f"schedu-teacher-{first_name[:3]}-{count:04}".lower()
