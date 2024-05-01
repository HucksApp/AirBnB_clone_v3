#!/usr/bin/python3
"""
FileStorage engine class
"""

import json
from models.base_model import BaseModel
from models.engine import serializable as classes


class FileStorage:
    """serializes and deserializes between object instances and json rep storage"""

    # string - path to the JSON file
    __file_path = "file.json"
    # dictionary - empty but will store all objects by <class name>.id
    __objects = {}

    def get(self, cls, id):
        """query for  one object"""
        if cls and (classes[cls] or cls in list(classes.keys())):
            for value in self.__objects.values():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    if value.id == id:
                        return value
        return None

    def count(self, cls=None):
        """query to count object of a class or all object in storage"""
        count = 0
        if cls and (classes[cls] or cls in list(classes.keys())):
            for value in self.__objects.values():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    count += 1
            return count
        return len(self.__objects)

    def all(self, cls=None):
        """returns private attribute: __objects"""
        if cls is not None:
            new_dict = {}
            for key, value in self.__objects.items():
                if cls == value.__class__ or cls == value.__class__.__name__:
                    new_dict[key] = value
            return new_dict
        return self.__objects

    def new(self, obj):
        """sets in __objects the obj with key <obj class name>.id"""
        if obj is not None:
            key = obj.__class__.__name__ + "." + obj.id
            self.__objects[key] = obj

    def save(self):
        """serializes __objects to the JSON file (path: __file_path)"""
        json_objects = {}
        for key in self.__objects:
            json_objects[key] = self.__objects[key].to_dict()
        with open(self.__file_path, 'w') as f:
            json.dump(json_objects, f)

    def reload(self):
        """if file exists, deserializes JSON file to __objects"""
        try:
            with open(self.__file_path, 'r') as f:
                jo = json.load(f)
            for key in jo:
                self.__objects[key] = classes[jo[key]["__class__"]](**jo[key])
        except:
            pass

    def delete(self, obj=None):
        """delete obj from __objects if it’s inside"""
        if obj is not None:
            key = obj.__class__.__name__ + '.' + obj.id
            if key in self.__objects:
                del self.__objects[key]

    def close(self):
        """call reload() method for deserializing the JSON file to objects"""
        self.reload()
