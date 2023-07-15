#!/usr/bin/python3
"""the class user to be defined"""
from models.base_model import BaseModel


class User(BaseModel):
    """
    to represent a user
    """
    email = ""
    password = ""
    first_name = ""
    last_name = ""
