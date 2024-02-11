#!/usr/bin/python3
"""Contains the class DBStorage
"""

import models
from models.base_model import BaseModel, Base
from models.admin import Admin
from models.teacher import Teacher
from models.student import Student
from models.guardian import Guardian
from os import getenv
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {
    "Teacher": Teacher,
    "Student": Student,
    "Guardian": Guardian,
    "Admin": Admin}


class DBStorage:
    """interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        MGT_MYSQL_USER = getenv('MGT_MYSQL_USER')
        MGT_MYSQL_PWD = getenv('MGT_MYSQL_PWD')
        MGT_MYSQL_HOST = getenv('MGT_MYSQL_HOST')
        MGT_MYSQL_DB = getenv('MGT_MYSQL_DB')
        MGT_ENV = getenv('MGT_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(MGT_MYSQL_USER,
                                             MGT_MYSQL_PWD,
                                             MGT_MYSQL_HOST,
                                             MGT_MYSQL_DB))
        if MGT_ENV == "test":
            Base.metadata.drop_all(self.__engine)


    def all(self, cls=None):
        """query on the current database session"""
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """add the object to the current database session"""
        self.__session.add(obj)

    def save(self):
        """commit all changes of the current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """delete from the current database session obj if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads data from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def get(self, cls, id):
        """retrieve one object"""
        if type(cls) == str:
            cls = classes[cls]
        return self.__session.query(cls).get(id)

    def count(self, cls=None):
        """count the number of objects in storage"""
        return self.__session.query(cls).count()

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
