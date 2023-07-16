#!/usr/bin/python3
'''
the model base class to be defined
'''
import uuid
import models
from datetime import datetime


class BaseModel:
    """a base in this project for all classes"""

    def __init__(self, *args, **kwargs):
        """an initialization of a public instance
         attribution"""
        if kwargs:
            for a, value in kwargs.items():
                if a == "created_at":
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if a == "updated_at":
                    value = datetime.strptime(value, '%Y-%m-%dT%H:%M:%S.%f')
                if a != "__class__":
                    setattr(self, a, value)
        else:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """a representaion string of this class
        to be returned"""
        nameClass = self.__class__.__name__
        return "[{}] ({}) {}".format(nameClass, self.id, self.__dict__)

    def save(self):
        """public instance attributes to be updates"""
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """__dict__ instance key/values to be returned"""
        copy_of_dict = self.__dict__.copy()
        copy_of_dict["created_at"] = self.created_at.isoformat()
        copy_of_dict["updated_at"] = self.updated_at.isoformat()
        copy_of_dict['__class__'] = self.__class__.__name__
        return copy_of_dict
