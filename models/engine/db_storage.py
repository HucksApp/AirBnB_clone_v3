#!/usr/bin/python3
"""DBStorage engine class"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.engine import serializable as classes
import os
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker


class DBStorage:
    """handles storage of all class instances with the MySQL database"""
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
        if os.environ.get("HBNB_ENV") == 'test':
            Base.metadata.drop_all(self.__engine)

    def get(self, cls, id):
        """
            query on the current database session
            for one object with given <id>
        """
        cls = (classes[cls] if type(cls) is str and cls in classes
               else cls if type(cls) in list(classes.values())
               else None)
        if cls:
            all_class = self.all(cls)
            for obj in all_class.values():
                if id == str(obj.id):
                    return obj
        return None

    def count(self, cls=None):
        """
            query on the current database session
            for counts of objects of a class or all
            objects in store
        """
        return len(self.all(cls))

    def all(self, cls=None):
        """returns a dictionary of all objects"""
        new_dict = {}

        if cls:
            objs = self.__session.query(classes.get(cls)).all()
            for obj in objs:
                print(obj)
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj
            return new_dict

        for clss in classes:
            if clss == 'BaseModel':
                continue
            objs = self.__session.query(classes.get(clss)).all()
            for obj in objs:
                print(obj.__dict__)
                key = obj.__class__.__name__ + '.' + obj.id
                new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """adds objects to current database session"""
        self.__session.add(obj)

    def save(self):
        """commits all changes of current database session"""
        self.__session.commit()

    def delete(self, obj=None):
        """deletes obj from current database session if not None"""
        if obj is not None:
            self.__session.delete(obj)

    def reload(self):
        """reloads all instance from the database"""
        Base.metadata.create_all(self.__engine)
        sess_factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(sess_factory)
        self.__session = Session

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()
