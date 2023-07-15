#!/usr/bin/python3
"""
console version 0.0.1
entry point of the command interpreter to be contained
"""

import sys
import cmd
import json
import models
import re
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    console class that is custom
    """

    prompt = '(hbnb)'

    def errors_of_mine(self, line, args_num):
        """
        error message to user to be displayed
        """
        classes = ["BaseModel", "User", "State", "City",
                   "Amenity", "Review", "Place"]

        msg = ["** class name missing **",
               "** class doesn't exist **",
               "** instance id missing **",
               "** no instance found **",
               "** attribute name missing **",
               "** value missing **"]
        if not line:
            print(msg[0])
            return 1
        args = line.split()
        if args_num >= 1 and args[0] not in classes:
            print(msg[1])
            return 1
        elif args_num == 1:
            return 0
        if args_num >= 2 and len(args) < 2:
            print(msg[2])
            return 1
        e = storage.all()

        for a in range(len(args)):
            if args[a][0] == '"':
                args[a] = args[a].replace('"', "")
        key = args[0] + '.' + args[1]
        if args_num >= 2 and key not in e:
            print(msg[3])
            return 1
        elif args_num == 2:
            return 0
        if args_num >= 4 and len(args) < 3:
            print(msg[4])
            return 1
        if args_num >= 4 and len(args) < 4:
            print(msg[5])
            return 1
        return 0

    def empty_line_handle(self, line):
        """
        empty lines to be eliminated
        """
        return True

    def do_quit(self, line):
        """the quit command to be handled"""
        return True

    def do_EOF(self, line):
        """command quit interpreter with ctrl+d"""
        return True

    def do_create(self, line):
        """a new instance of @cls_name class
        to be created"""
        if (self.errors_of_mine(line, 1) == 1):
            return
        args = line.split(" ")
        obj = eval(args[0])()
        obj.save()

        print(obj.id)

    def do_show(self, line):
        """a string representaion of an instance
         to be printed"""
        if (self.errors_of_mine(line, 2) == 1):
            return
        args = line.split()
        e = storage.all
        if args[1][0] == '"':
            args[1] = args[1].replace('"', "")
        key = args[0] + '.' + args[1]
        print(e[key])

    def do_destroy(self, line):
        """an instance of a certqin class
        to be deleted"""
        if (self.errors_of_mine(line, 2) == 1):
            return
        args = line.split()
        e = storage.all()
        if args[1][0] == '"':
            args[1] = args[1].replace('"', "")
        key = args[0] + '.' + args[1]
        del e[key]
        storage.save()

    def do_all(self, line):
        """instance of a certain class
        or all instances to be showed"""
        e = storage.all()
        if not line:
            print([str(a) for a in e.values()])
            return
        args = line.split()
        if (self.errors_of_mine(line, 1) == 1):
            return
        print([str(b) for b in e.values()
               if b.__class__.__name__ == args[0]])

    def do_update(self, line):
        """an instance of class ir id to be updated
        based on it"""
        if (self.errors_of_mine(line, 4) == 1):
            return
        args = line.split()
        e = storage.all()
        for a in range(len(args[1:]) + 1):
            if args[a][0] == '"':
                args[a] = args[a].replace('"', "")
        key = args[0] + '.' + args[1]
        attr_a = args[2]
        attr_b = args[3]
        try:
            if attr_b.isdigit():
                attr_b = int(attr_b)
            elif float(attr_b):
                attr_b = float(attr_b)
        except ValueError:
            pass
        class_atr = type(e[key]).__dict__
        if attr_a in class_atr.keys():
            try:
                attr_b = type(class_atr[attr_a])(attr_b)
            except Exception:
                print("Entered wrong value type")
                return
        setattr(e[key], attr_a, attr_b)
        storage.save()

    def count(self, n_class):
        """method that instances of a certain
        classes to be count"""
        count_instance = 0
        for obj_ins in storage.all().values():
            if obj_ins.__class__.__name__ == n_class:
                count_instance += 1
        print(count_instance)

    def default(self, line):
        """to take care of several
        commands method"""
        names = ["BaseModel", "User", "State", "Amenity", "City",
                 "Review", "Place"]
        commands = {"count": self.count,
                    "all": self.do_all,
                    "destroy": self.do_destroy,
                    "update": self.do_update,
                    "show": self.do_show}

        args = re.match(r"^(\w+)\.(\w+)\((.*)\)", line)
        if args:
            args = args.groups()
        if not args or len(args) < 2 or args[0] not in names \
                or args[1] not in commands.keys():
            super.default(line)

        if args[1] in ["all", "count"]:
            commands[args[1]](args[0])
        elif args[1] in ["destroy", "show"]:
            commands[args[1]](args[0] + ' ' + args[2])
        elif args[1] == "update":
            parameter = re.match(r"\"(.+?)\", (.+)", args[2])
            if parameter.groups()[1][0] == '{':
                diction_p = eval(parameter.groups()[1])
                for a, b in diction_p.items():
                    commands[args[1]](args[0] + " " + parameter.groups()[0] +
                                      " " + a + " " + str(b))
            else:
                remaining = parameter.groups()[1].split(", ")
                commands[args[1]](args[0] + " " + parameter.groups()[0] +
                                  " " + remaining[0] + " " + remaining[1])


if __name__ == '__main__':
    HBNBCommand().cmdloop()
