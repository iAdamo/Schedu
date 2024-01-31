import models
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

class DBStorage:
    """Interacts with the MySQL database"""
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a DBStorage object"""
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'.
                                      format(HBNB_MYSQL_USER,
                                             HBNB_MYSQL_PWD,
                                             HBNB_MYSQL_HOST,
                                             HBNB_MYSQL_DB))
        if HBNB_ENV == "test":
            models.Base.metadata.drop_all(self.__engine)

    def get_session(self):
        """Return the current database session"""
        if self.__session is None:
            self.__session = scoped_session(sessionmaker(bind=self.__engine, expire_on_commit=False))
        return self.__session()

    def all(self, cls=None):
        """Query on the current database session"""
        new_dict = {}
        session = self.get_session()
        if cls:
            objs = session.query(cls).all()
            for obj in objs:
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj
        else:
            for clss in models.Base.__subclasses__():
                objs = session.query(clss).all()
                for obj in objs:
                    key = obj.__class__.__name__ + '.' + obj.id
                    new_dict[key] = obj
        return new_dict

    def new(self, obj):
        """Add the object to the current database session"""
        session = self.get_session()
        session.add(obj)

    def save(self):
        """Commit all changes of the current database session"""
        session = self.get_session()
        session.commit()

    def delete(self, obj=None):
        """Delete from the current database session obj if not None"""
        if obj:
            session = self.get_session()
            session.delete(obj)

    def reload(self):
        """Reloads data from the database"""
        models.Base.metadata.create_all(self.__engine)

    def get(self, cls, id):
        """Retrieve one object"""
        session = self.get_session()
        try:
            return session.query(cls).filter(cls.id == id).one()
        except sqlalchemy.orm.exc.NoResultFound:
            return None

    def count(self, cls=None):
        """Count the number of objects in storage"""
        session = self.get_session()
        if cls:
            return session.query(cls).count()
        return sum(session.query(clss).count() for clss in models.Base.__subclasses__())

    def close(self):
        """Close the current database session"""
        if self.__session is not None:
            self.__session.remove()