#!/usr/bin/python3
""" Holds class Student """

import models
from models.base_model import BaseModel, Base
from os import getenv
from sqlalchemy import Column, Integer, String, ForeignKey
from sqlalchemy.orm import relationship
from flask_login import UserMixin


class Student(UserMixin, BaseModel, Base):
    """Representation of student
    """

    if models.storage_type == "db":
        __tablename__ = 'students'
        id = Column(String(60), nullable=False, primary_key=True)
        password = Column(String(128), nullable=False)
        name = Column(String(60), nullable=False)
        address = Column(String(128), nullable=False)
        date_of_birth = Column(String(10), nullable=False)
        nin = Column(Integer, nullable=False, unique=True)
        phone_number = Column(Integer, nullable=False, unique=True)
        email = Column(String(128), nullable=False, unique=True)
        role = Column(String(128), nullable=False)
        guardian_id = Column(String(60), ForeignKey('guardians.id'))
        guardian_relation = relationship("Guardian", backref="students", foreign_keys=[guardian_id])
    else:
        def __init__(self, *args, **kwargs):
            """ Initializes student """
            super().__init__(*args, **kwargs)
