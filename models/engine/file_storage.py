"""
This module defines the FileStorage class for serializing and deserializing
objects to and from a JSON file.

This file contains the FileStorage class, which is responsible for saving and
loading objects to and from a JSON file. It defines methods for saving objects
to the file, loading objects from the file, and retrieving objects by class
and ID. It also defines methods for deleting objects and counting the number
of objects stored in the file.
"""

import json
from models.amenity import Amenity
from models.base_model import BaseModel
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
from models.user import User


# Define a dictionary mapping class names to their corresponding model classes
classes = {"Amenity": Amenity, "BaseModel": BaseModel, "City": City,
           "Place": Place, "Review": Review, "State": State, "User": User}


class FileStorage:
    """Serializes and deserializes objects to and from a JSON file.

    This class is responsible for saving and loading objects to and from a JSON
    file. It defines methods for saving objects to the file, loading objects
    from the file, retrieving objects by class and ID, deleting objects, and
    counting the number of objects stored in the file.
    """
    # The path to the JSON file where objects are stored
    __file_path = "file.json"
    # A dictionary mapping object IDs to the corresponding objects
    __objects = {}

    def all(self, cls=None):
        """Returns a dictionary of all objects stored in the file.
        This method returns a dictionary mapping object IDs to the
        corresponding objects for all objects stored in the file.
        If a class is specified,it returns a dictionary of all
        objects of that class only.
        """
        if cls is not None:
            return {
                key: value
                for key, value in self.__objects.items()
                if cls in [value.__class__, value.__class__.__name__]
            }
        return self.__objects

    def new(self, obj):
        """Adds a new object to the dictionary of objects stored in the file.
        This method adds a new object to the dictionary of objects stored
        in the file. It uses the object's class name and ID to create a key
        for the dictionary entry.
        """
        if obj is not None:
            key = f"{obj.__class__.__name__}.{obj.id}"
            self.__objects[key] = obj

    def save(self):
        """Serializes all objects to the JSON file. This method
        serializes all objects in the dictionary of objects stored
        in the file to a JSON-formatted string and writes the string
        to the file specified by __file_path.
        """
        json_objects = {key: self.__objects[key].to_dict() for key in self.__objects}
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """Deserializes all objects from the JSON file.

        This method reads the JSON-formatted string from the file specified by
        __file_path and deserializes the objects back into Python objects. It
        stores the objects in the dictionary of objects stored in the file.
        """
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if its inside"""
        if obj is not None:
            key = f'{obj.__class__.__name__}.{obj.id}'
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()

    def get(self, cls, id):
        """Returns the object based on the class and its ID"""
        if cls not in classes.values():
            return None

        list_obj = self.all(cls).values()
        for obj in list_obj:
            if obj.id == id:
                return obj

    def count(self, cls=None):
        """Returns the number of objects in storage"""
        return len(self.all()) if cls is None else len(self.all(cls))
