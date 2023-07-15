#!/usr/bin/python3
"""
review class to be defined
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    a review to be represented
    """
    place_id = ""
    user_id = ""
    text = ""
