#!/usr/bin/python3
""" a module unit test"""

import sys
import unittest
import os
from io import StringIO
from unittest.mock import create_autospec, patch
from models import storage
from console import HBNBCommand
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class ConsoleTest(unittest.TestCase):
    """console model Unittest"""

    def setUp(self):
        """stdin and stdout to
        be redirected"""
        self.mock_stdout = create_autospec(sys.stdout)
        self.mock_stdin = create_autospec(sys.stdin)
        self.error = ["** class name missing **",
                      "** class doesn't exist **",
                      "** instance id missing **",
                      "** no instance found **",]

        self.clas = ["BaseModel",
                     "User",
                     "State",
                     "City",
                     "Place",
                     "Amenity",
                     "Review"]

    def make(self, server=None):
        """to the mock module
        stdin and stdout to
        be redirected"""
        return HBNBCommand(stdin=self.mock_stdin, stdout=self.mock_stdout)

    def write_last(self, lw=None):
        """ last num output lines
        to be returned"""
        if lw is None:
            return self.mock_stdout.write.call_args[0][0]
        return "".join(map(lambda a: a[0][0],
                           self.mock_stdout.write.call_args_list[-lw:]))

    def test_quit(self):
        """command quit"""
        client = self.make()
        self.assertTrue(client.onecmd("quit"))


if __name__ == '__main__':
    unittest.main()
