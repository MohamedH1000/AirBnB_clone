#!/usr/bin/pyhton3
"""file storage test"""
import pep8
import json
import os
import unittest
from models.base_model import BaseModel
from models.engine.file_storage import FileStorage
from models.review import Review
from models.user import User
from models.place import Place
from models.state import State
from models.amenity import Amenity
from models.city import City


class FileStorageTest(unittest.TestCase):
    """the file storage to be tested"""

    @classmethod
    def setUpClass(cls):
        """for test to be setup"""
        cls.user = User()
        cls.user.first_name = "mohamed"
        cls.user.last_name = "Hesham"
        cls.user.email = "mohammedhisham115@gmail.com"
        cls.storage = FileStorage()

    @classmethod
    def teardown(cls):
        """this will teat it down
        at the end of the test"""
        del cls.user

    def tearDown(self):
        """teardown"""
        try:
            os.remove("file.json")
        except Exception:
            pass

    def test_pep8_FileStorage(self):
        """pep8 style to be tested"""
        style = pep8.StyleGuide(quiet=True)
        a = style.check_files(['models/engine/file_storage.py'])
        self.assertEqual(a.total_errors, 0, "fix pep8")

    def test_all(self):
        """if all works in File Storage
        to be tested"""
        storage = FileStorage()
        obj = storage.all()
        self.assertIsNotNone(obj)
        self.assertEqual(type(obj), dict)
        self.assertIs(obj, storage._FileStorage__objects)

    def test_new(self):
        """when new is created
        to be tested"""
        storage = FileStorage()
        obj = storage.all()
        user = User()
        user.id = 987652
        user.name = "mohamed"
        storage.new(user)
        key = user.__class__.__name__ + "." + str(user.id)
        self.assertIsNotNone(obj[key])

    def test_reload_FileStorage(self):
        """test reload"""
        self.storage.save()
        origin = os.path.dirname(os.path.abspath("console.py"))
        path = os.path.join(origin, "file.json")
        with open(path, 'r') as File:
            lines = File.readlines()
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
        self.storage.save()
        with open(path, 'r') as File:
            lines2 = File.readlines()
        self.assertEqual(lines, lines2)
        try:
            os.remove(path)
        except FileNotFoundError:
            pass
        with open(path, "w") as File:
            File.write("{}")
        with open(path, "r") as readable:
            self.assertEqual(lines, "{}")
        self.assertIs(self.storage.reload(), None)


if __name__ == '__main__':
    unittest.main()
