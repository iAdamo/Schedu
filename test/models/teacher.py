#!/usr/bin/python3
""" holds class Teacher"""
import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, String, ForeignKey
from sqlalchemy.orm import relationship


class Teacher(BaseModel, Base):
    """Representation of teacher"""
    if models.storage_type == "db":
        __tablename__ = 'teachers'
        id = Column(String(60), nullable=False, primary_key=True)
        name = Column(String(128), nullable=False)
        subject = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
    else:
        id = ""
        name = ""
        subject = ""
        email = ""

    def __init__(self, *args, **kwargs):
        """initializes teacher"""
        super().__init__(*args, **kwargs)
