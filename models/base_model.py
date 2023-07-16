#!/usr/bin/python3
from datetime import datetime
from uuid import uuid4
import models

"""
the base for all classes in the airbnb project
"""


class BaseModel():
    """
    basic class for all other classes
    """

    def __init__(self, *args, **kwargs):
        """
        attributes to be initialized
        """
        date_format = '%Y-%m-%dT%H:%M:%S.%f'
        if kwargs:
            for a, value in kwargs.items():
                if "created_at" == a:
                    self.created_at = datetime.strptime(kwargs["created_at"],
                                                        date_format)
                elif "updated_at" == a:
                    self.updated_at = datetime.strptime(kwargs["updated_at"],
                                                        date_format)
                elif "__class__" == a:
                    pass
                else:
                    setattr(self, a, value)
        else:
            self.id = str(uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
            models.storage.new(self)

    def __str__(self):
        """
        return str
        """
        return ('[{}] ({}) {}'.
                format(self.__class__.__name__, self.id, self.__dict__))

    def __repr__(self):
        """
        repr string to be returned
        """
        return (self.__str__())

    def save(self):
        """
        save to serialize file
        """
        self.updated_at = datetime.now()
        models.storage.save()

    def to_dict(self):
        """
        return dictionary
        """
        diction = self.__dict__.copy()
        diction["created_at"] = self.created_at.isoformat()
        diction["updated_at"] = self.updated_at.isoformat()
        diction["__class__"] = self.__class__.__name__
        return diction
