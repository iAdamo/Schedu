#!/usr/bin/python3
""" holds class Admin"""
import models
from models.base_model import BaseModel, Base
from os import getenv
import sqlalchemy
from sqlalchemy import Column, String


class Admin(BaseModel, Base):
    """Representation of admin """
    if models.storage_type == "db":
        __tablename__ = 'admins'
        id = Column(String(60), nullable=False, primary_key=True)
        name = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False)
        role = Column(String(128), nullable=False)
    else:
        id = ""
        name = ""
        email = ""
        role = ""

    def __init__(self, *args, **kwargs):
        """initializes admin"""
        super().__init__(*args, **kwargs)
