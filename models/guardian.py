#!/usr/bin/python3
""" Holds class Guardian """

import models
from models.base_model import BaseModel, Base
from models.student import Student
from os import getenv
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class Guardian(UserMixin, BaseModel, Base):
    """ Representation of guardian """
    if models.storage_type == "db":
        __tablename__ = 'guardians'
        id = Column(String(60), nullable=False, primary_key=True)
        password = Column(String(128), nullable=False)
        name = Column(String(60), nullable=False)
        date_of_birth = Column(String(10), nullable=False)
        nin = Column(Integer, nullable=False, unique=True)
        phone_number = Column(Integer, nullable=False, unique=True)
        email = Column(String(128), nullable=False, unique=True)
        role = Column(String(128), nullable=False)
        student_id = Column(String(60), ForeignKey('students.id'), nullable=False)
        student_relation = relationship("Student", backref="guardian", foreign_keys=[student_id])
    else:
        def __init__(self, *args, **kwargs):
            """ Initializes guardian """
            super().__init__(*args, **kwargs)
