#!/usr/bin/python3
'''
the model base class to be defined
'''
import models
from datetime import datetime
from uuid import uuid4


class BaseModel:
    """a base in this project for all classes"""

    def __init__(self, *args, **kwargs):
        """an initialization of a public instance
         attribution"""

        FORMAT_DATA_TIME = '%Y-%m-%dT%H:%M:%S.%f'
        if not kwargs:
            self.id = str(uuid4())
            self.created_at = datetime.utcnow()
            self.updated_at = datetime.utcnow()
            models.storage.new(self)
        else:
            for key, value in kwargs.items():
                if key in ("updated_at", "created_at"):
                    self.__dict__[key] = datetime.strptime(
                        value, FORMAT_DATA_TIME)
                elif key[0] == "id":
                    self.__dict__[key] = str(value)
                else:
                    self.__dict__[key] = value

    def __str__(self):
        """a representaion string of this class
        to be returned"""
        return "[{}] ({}) {}".format(self.__class__.__name__,
                                     self.id, self.__dict__)

    def save(self):
        """public instance attributes to be updates"""
        self.updated_at = datetime.utcnow()
        models.storage.save

    def to_dict(self):
        """__dict__ instance key/values to be returned"""
        object_of_a_map = {}
        for key, value in self.__dict__.items():
            if key == "created_at" or key == "updated_at":
                object_of_a_map[key] = value.isoformat()
            else:
                object_of_a_map[key] = value
        object_of_a_map["__class__"] = self.__class__.__name__
        return object_of_a_map
