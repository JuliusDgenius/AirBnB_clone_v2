#!/usr/bin/python3
# Database storage with sqlalchemy and MYSQL
from models.base_model import Base
from models.user import User
from models.state import State
from models.place import Place
from models.review import Review
from models.city import City
from models.amenity import Amenity
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, scoped_session
from os import getenv

classes_dict = {
    'Amenity': Amenity,
    'City': City,
    'Place': Place,
    'State': State,
    'Review': Review,
    'User': User
}


class DBStorage:
    """
    Database class that define the SQALalchemy plus mysql database
    """
    __engine = None
    __session = None

    def __init__(self):
        """
        Initializes the database instance/object
        """
        user = getenv('HBNB_MYSQL_USER')
        passwd = getenv('HBNB_MYSQL_PWD')
        host = getenv('HBNB_MYSQL_HOST')
        db = getenv('HBNB_MYSQL_DB')

        self.__engine = create_engine('mysql+mysqldb://{}:{}@{}/{}'
                                      .format(user, passwd, host, db),
                                      pool_pre_ping=True)

        if getenv('HBNB_ENV') == 'test':
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Retrieves all records in the database
        """
        if not self.__session:
            self.reload()
        _objects = {}
        if type(cls) == str:
            cls = classes_dict.get(cls, None)
        if cls:
            for obj in self.__session.query(cls):
                _objects[obj.__class__.__name__ + '.' + obj.id] = obj
        else:
            for cls in classes_dct.values():
                for obj in self.__session.query(cls):
                    _objects[obj.__class__.__name__ + '.' + obj.id] = obj
        return _objects

    def new(self, obj):
        """Public method to create a new object"""
        self.__session.add(obj)

    def save(self):
        """Public method to save the current session"""
        self.__session.commit()

    def delete(self, obj=None):
        """Public method to delete an object"""
        if not self.__session:
            self.reload()
        if obj:
            self.__session.delete(obj)

    def reload(self):
        """Public method to reload object from the database"""
        make_session = sessionmaker(bind=self.__engine,
                                    expire_on_commit=False)
        Base.metadata.create_all(self.__engine)
        self.__session = scoped_session(make_session)

    def close(self):
        """Dispose of current session if active"""
        self.__session.remove()

    def get(self, cls, id):
        """Retrieve an object"""
        if cls is not None and type(cls) is str and id is not None and\
           type(id) is str and cls in classes_dct:
            cls = classes_dct[cls]
            result = self.__session.query(cls).filter(cls.id == id).first()
            return result
        else:
            return None

    def count(self, cls=None):
        """Count number of objects in storage"""
        total = 0
        if type(cls) is str and cls in classes_dct:
            cls = classes_dct[cls]
            total = self.__session.query(cls).count()
        elif cls is None:
            for cls in classes_dct.values():
                total += self.__session.query(cls).count()
        return total
