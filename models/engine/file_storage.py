#!/usr/bin/python3
"""serialize and deserialize json types
by this module file storage"""

from models.base_model import BaseModel
from models.user import User
import json


class FileStorage:
    """for file storage custom class"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """all objects dictionary representation
        to be returned"""
        return self.__objects

    def new(self, object):
        """in object the object with ket to be set"""
        self.__objects[object.__class__.__name__ + '.' + str(object)] = object

    def save(self):
        """ objects to the json file
        to be serialized"""
        with open(self.__file_path, 'w+') as File:
            json.dump({k: v.to_dict() for k, v in self.__objects.items()
                       }, File)

    def reload(self):
        """
        the json file to objects to be deserialized
        """
        try:
            with open(self.__file_path, 'r') as File:
                dict = json.loads(File.read())
                for value in dict.values():
                    cls = value["__class__"]
                    self.new(eval(cls)(**value))
        except Exception:
            pass
