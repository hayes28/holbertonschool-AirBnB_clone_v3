#!/usr/bin/python3
"""
This module defines the DBStorage class for interacting with a MySQL database.

This file contains the DBStorage class, which is responsible for interacting
with a MySQL database to store and retrieve objects. It uses SQLAlchemy to
handle database connections and queries, and defines methods for querying,
adding, deleting, and saving objects in the database.
"""

import models
from models.amenity import Amenity
from models.base_model import BaseModel, Base
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User
from os import getenv
import sqlalchemy
from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

classes = {"Amenity": Amenity, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class DBStorage:
    """Interacts with a MySQL database to store and retrieve objects.

    This class is responsible for managing the connection to a MySQL
    database and providing methods for interacting with the data stored
    in the database. It defines methods for querying, adding, deleting,
    and saving objects in the database, as well as loading data from the
    database and handling database sessions.
    """
    __engine = None
    __session = None

    def __init__(self):
        """Instantiate a new DBStorage object.

        This method creates a new DBStorage object and initializes the database
        connection using the values of environment variables. If the HBNB_ENV
        environment variable is set to "test", it drops all tables from the
        database before creating a new connection.
        """
        HBNB_MYSQL_USER = getenv('HBNB_MYSQL_USER')
        HBNB_MYSQL_PWD = getenv('HBNB_MYSQL_PWD')
        HBNB_MYSQL_HOST = getenv('HBNB_MYSQL_HOST')
        HBNB_MYSQL_DB = getenv('HBNB_MYSQL_DB')
        HBNB_ENV = getenv('HBNB_ENV')
        self.__engine = create_engine(
            f'mysql+mysqldb://{HBNB_MYSQL_USER}:{HBNB_MYSQL_PWD}@{HBNB_MYSQL_HOST}/{HBNB_MYSQL_DB}'
        )
        if HBNB_ENV == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """Returns a dictionary of all objects in the database.

        This method queries the database for all objects of a particular class
        or for all objects if no class is specified. It returns a dictionary
        mapping object IDs to the corresponding objects.
        """
        new_dict = {}
        for clss in classes:
            if cls is None or cls is classes[clss] or cls is clss:
                objs = self.__session.query(classes[clss]).all()
                for obj in objs:
                    key = f'{obj.__class__.__name__}.{obj.id}'
                    new_dict[key] = obj
        return (new_dict)

    def new(self, obj):
        """Adds an object to the current database session.

        This method adds a new object to the current database session.
        The object is not saved to the database until the save()
        method is called.
        """
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

    def close(self):
        """call remove() method on the private session attribute"""
        self.__session.remove()

    def get(self, cls, id):
        """Returns an object matching class and id"""
        if cls in classes.values():
            return self.__session.query(cls).filter(cls.id == id).first()
        return None

    def count(self, cls=None):
        """Counts number of objects"""
        return len(self.all(cls))
