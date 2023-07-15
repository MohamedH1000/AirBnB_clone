#!/usr/bin/python3
"""base model suit
 to be tested"""

import unittest
import os
import json
import re
import uuid
from datetime import datetime
from models.base_model import BaseModel
from time import sleep


class BaseModelTest(unittest.TestCase):
    """base model attribute to be tested"""

    def setUp(self):
        """the classes that
        are needed for testing"""
        pass

    def test_basic(self):
        """basic model class basic input
        to be tested"""
        model_of_mine = BaseModel()
        model_of_mine.name = "ALX"
        model_of_mine.number = 45
        self.assertEqual([model_of_mine.name, model_of_mine.number],
                         ["ALX", 45])

    def test_determine(self):
        """correct datetime format
        to be tested"""
        pass

    def test_datetime(self):
        """correct datetime format to
        be tested"""
        pass


if __name__ == '__main__':
    unittest.main
