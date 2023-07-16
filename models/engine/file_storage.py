#!/usr/bin/python3
"""serialize and deserialize json types
by this module file storage"""

from models.base_model import BaseModel
from models.user import User
from models.amenity import Amenity
from models.city import City
from models.place import Place
from models.review import Review
from models.state import State
import json


class FileStorage:
    """for file storage custom class"""

    __file_path = "file.json"
    __objects = {}

    def all(self):
        """all objects dictionary representation
        to be returned"""
        return self.__objects

    def new(self, obj):
        """in object the object with ket to be set"""
        key = obj.__class__.__name__ + '.' + str(obj.id)
        self.__objects[key] = obj

    def save(self):
        """ objects to the json file
        to be serialized"""
        json_object = {}
        for a in self.__objects:
            json_object[a] = self.__objects[a].to_dict()

        with open(self.__file_path, 'w') as File:
            json.dump(json_object, File)

    def reload(self):
        """
        the json file to objects to be deserialized
        """
        try:
            with open(self.__file_path, 'r', encoding='UTF8') as File:
                for a, value in json.load(File).items():
                    attributed_value = eval(value["__class__"])(**value)
                    self.__objects[a] = attributed_value
        except FileNotFoundError:
            pass
