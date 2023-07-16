#!/usr/bin/python3
"""
console version 0.0.1
entry point of the command interpreter to be contained
"""

import sys
import cmd
import shlex
import json
import models
import re
from models.base_model import BaseModel
from models.user import User
from models.city import City
from models.amenity import Amenity
from models.place import Place
from models.review import Review
from models.state import State
from models import storage


class HBNBCommand(cmd.Cmd):
    """
    console class that is custom
    """

    prompt = '(hbnb)'

    classes = {'BaseModel': BaseModel, 'Amenity': Amenity,
               'State': State, 'Place': Place, 'Review': Review,
               'User': User, 'City': City}

    def empty_line_handle(self):
        """
        empty lines to be eliminated
        """
        pass

    def do_quit(self, line):
        """the quit command to be handled"""
        return True

    def do_EOF(self, line):
        """command quit interpreter with ctrl+d"""
        print()
        return True

    def do_create(self, argum):
        """a new instance of @cls_name class
        to be created"""
        if argum:
            if argum in self.classes:
                class_get = getattr(sys.modules[__name__], argum)
                moment = class_get
                print(moment.id)
                models.storage.save()
            else:
                print("** class doesn't exist **")
        else:
            print("** class name missing **")
        return

    def do_show(self, argum):
        """a string representaion of an instance
         to be printed"""
        nums = shlex.split(argum)
        if len(nums) == 0:
            print("** class name missing **")
        elif len(nums) == 1:
            print("** instance id missing **")
        elif nums[0] not in self.classes:
            print("** class doesn't exist **")
        else:
            dic = models.storage.all()
            keyyy = nums[0] + '.' + str(nums[1])
            if keyyy in dic:
                print(dic[keyyy])
            else:
                print("** no instance found **")
        return

    def do_destroy(self, argum):
        """an instance of a certqin class
        to be deleted"""
        nums4 = shlex.split(argum)
        if len(nums4) == 0:
            print("** class name missing **")
            return
        elif len(nums4) == 1:
            print("** instance id missing **")
            return
        elif nums4[0] not in self.classes:
            print("** class doesn't exist **")
            return
        else:
            dic = models.storage.all()
            keyyy = nums4[0] + '.' + nums4[1]
            if keyyy in dic:
                del dic[keyyy]
                models.storage.save()
            else:
                print("** no instance found **")

    def do_all(self, argum):
        """instance of a certain class
        or all instances to be showed"""
        nums1 = shlex.split(argum)
        listA = []
        dic = models.storage.all()
        if len(nums1) == 0:
            for a in dic:
                Class_representaion = str(dic[a])
                listA.append(Class_representaion)
            print(listA)
            return

        if nums1[0] not in self.classes:
            print("** class doesn't exist **")
            return
        else:
            Class_representaion = ""
            for a in dic:
                Nameclass = a.split('.')
                if Nameclass[0] == nums1[0]:
                    Class_representaion = str(dic[a])
                    listA.append(Class_representaion)
            print(listA)

    def do_update(self, argum):
        """an instance of class ir id to be updated
        based on it"""
        numsU = shlex.split(argum)
        if len(numsU) == 0:
            print("** class name missing **")
            return
        elif len(numsU) == 1:
            print("** instance id missing **")
            return
        elif len(numsU) == 2:
            print("** attribute name missing **")
            return
        elif len(numsU) == 3:
            print("** value missing **")
            return
        elif numsU[0] not in self.classes:
            print("** class doesn't exist **")
            return
        keyA = numsU[0] + '.' + numsU[1]
        dicA = models.storage.all()
        try:
            momentU = dicA[keyA]
        except KeyError:
            print("** no instance found **")
            return
        try:
            branchA = type(getattr(momentU, numsU[2]))
            numsU[3] = branchA(numsU[3])
        except AttributeError:
            pass
        setattr(momentU, numsU[2], numsU[3])
        models.storage.save()

    def count(self, argum):
        """method that instances of a certain
        classes to be count"""
        numsA = shlex.split(argum)
        dic = models.storage.all()
        moment_num = 0
        if numsA[0] not in self.classes:
            print("** class doesn't exist **")
            return
        else:
            for a in dic:
                Nameclass = a.split('.')
                if Nameclass[0] == numsA[0]:
                    moment_num += 1

            print(moment_num)

    def precmd(self, argum):
        """before the command line is executed"""
        args = argum.split('.', 1)
        if len(args) == 2:
            _class = args[0]
            args = args[1].split('(', 1)
            command = args[0]
            if len(args) == 2:
                args = args[1].split(')', 1)
                if len(args) == 2:
                    _id = args[0]
                    argu_other = args[1]
            line = command + " " + _class + " " + _id + " " + argu_other
            return line
        else:
            return argum


if __name__ == '__main__':
    HBNBCommand().cmdloop()
