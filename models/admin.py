#!/usr/bin/python3
""" Holds class Admin """

import models
from models.base_model import BaseModel, Base
from os import getenv
from flask_login import UserMixin
from sqlalchemy import Column, String


class Admin(UserMixin, BaseModel, Base):
    """ Representation of admin """
    if models.storage_type == "db":
        __tablename__ = 'admins'
        id = Column(String(60), nullable=False, primary_key=True)
        name = Column(String(128), nullable=False)
        email = Column(String(128), nullable=False, unique=True)
        role = Column(String(128), nullable=False)
    else:
        id = ""
        name = ""
        email = ""
        role = "admin"

    def __init__(self, *args, **kwargs):
        """ Initializes admin
        """
        super().__init__(*args, **kwargs)
        first_name = kwargs.get("first_name", "")
        from models import storage
        count = len(storage.all("Admin"))
        self.id = f"schedu-admin-{first_name[:3]}-{str(count).zfill(4)}".lower(
        )

    def is_active(self):
        """ Return True if the user account is active, and False otherwise """
        return True
