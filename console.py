#!/usr/bin/python3
"""hbnb console to be defined"""
import cmd
import re
from shlex import split
from models import storage
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


def parse(argum):
    aqwas_mkt = re.search(r"\{(.*?)\}", argum)
    brackets = re.search(r"\[(.*?)\]", argum)
    if aqwas_mkt is None:
        if brackets is None:
            return [i.strip(",") for i in split(argum)]
        else:
            lexer = split(argum[:brackets.span()[0]])
            returnl = [i.strip(",") for i in lexer]
            returnl.append(brackets.group())
            return returnl
    else:
        lexer = split(argum[:aqwas_mkt.span()[0]])
        returnl = [i.strip(",") for i in lexer]
        returnl.append(aqwas_mkt.group())
        return returnl


class HBNBCommand(cmd.Cmd):
    """
    hbnb console to be defined
    """

    prompt = "(hbnb) "

    __classes = {
        "BaseModel",
        "User",
        "State",
        "City",
        "Place",
        "Amenity",
        "Review"
    }

    def emptyline(self):
        """just recieve an empty line"""
        pass

    def default(self, argum):
        """Default behaviour"""
        argumentdictionary = {
            "all": self.do_all,
            "show": self.do_show,
            "destroy": self.do_destroy,
            "count": self.do_count,
            "update": self.do_update
        }
        connect = re.search(r"\.", argum)
        if connect is not None:
            arl = [argum[:connect.span()[0]], argum[connect.span()[1]:]]
            connect = re.search(r"\((.*?)\)", arl[1])
            if connect is not None:
                command = [arl[1][:connect.span()[0]], connect.group()[1:-1]]
                if command[0] in argumentdictionary.keys():
                    call = "{} {}".format(arl[0], command[1])
                    return argumentdictionary[command[0]](call)
        print("*** Unknown syntax: {}".format(argum))
        return False

    def do_quit(self, arg):
        """a quit command"""
        return True

    def do_EOF(self, arg):
        """exit the program by this eof command"""
        print("")
        return True

    def do_create(self, line):
        """
        a create function
        """
        try:
            if not line:
                raise SyntaxError()
            list_of_mine = line.split(" ")

            kwargs = {}
            for a in range(1, len(list_of_mine)):
                k, value = tuple(list_of_mine[a].split("="))
                if value[0] == '"':
                    value = value.strip('"').replace("_", " ")
                else:
                    try:
                        value = eval(value)
                    except (SyntaxError, NameError):
                        continue
                kwargs[k] = value

            if kwargs == {}:
                objec = eval(list_of_mine[0])()
            else:
                objec = eval(list_of_mine[0])(**kwargs)
                storage.new(objec)
            print(objec.id)
            objec.save()

        except SyntaxError:
            print("** class name missing **")
        except NameError:
            print("** class doesn't exist **")

    def do_show(self, argum):
        """to show string representaion
        """
        argumentl = parse(argum)
        dictionary_obj = storage.all()
        if len(argumentl) == 0:
            print("** class name missing **")
        elif argumentl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(argumentl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(argumentl[0], argumentl[1]) not in dictionary_obj:
            print("** no instance found **")
        else:
            print(dictionary_obj["{}.{}".format(argumentl[0], argumentl[1])])

    def do_destroy(self, argum):
        """to delete a class
        instance of an id that is given"""
        arl = parse(argum)
        dictionary_obj = storage.all()
        if len(arl) == 0:
            print("** class name missing **")
        elif arl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        elif len(arl) == 1:
            print("** instance id missing **")
        elif "{}.{}".format(arl[0], arl[1]) not in dictionary_obj.keys():
            print("** no instance found **")
        else:
            del dictionary_obj["{}.{}".format(arl[0], arl[1])]
            storage.save()

    def do_all(self, argum):
        """of all instances string representaion"""
        arl = parse(argum)
        if len(arl) > 0 and arl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
        else:
            objectl = []
            for obj in storage.all().values():
                if len(arl) > 0 and arl[0] == obj.__class__.__name__:
                    objectl.append(obj.__str__())
                elif len(arl) == 0:
                    objectl.append(obj.__str__())
            print(objectl)

    def do_count(self, argum):
        """to calculate the number
        of instances at a class"""
        argumentl = parse(argum)
        seehwmnm = 0
        for obj in storage.all().values():
            if argumentl[0] == obj.__class__.__name__:
                seehwmnm += 1
        print(seehwmnm)

    def do_update(self, argum):
        """update function"""
        arl = parse(argum)
        dictionary_obj = storage.all()

        if len(arl) == 0:
            print("** class name missing **")
            return False
        if arl[0] not in HBNBCommand.__classes:
            print("** class doesn't exist **")
            return False
        if len(arl) == 1:
            print("** instance id missing **")
            return False
        if "{}.{}".format(arl[0], arl[1]) not in dictionary_obj.keys():
            print("** no instance found **")
            return False
        if len(arl) == 2:
            print("** attribute name missing **")
            return False
        if len(arl) == 3:
            try:
                type(eval(arl[2])) != dict
            except NameError:
                print("** value missing **")
                return False

        if len(arl) == 4:
            obj = dictionary_obj["{}.{}".format(arl[0], arl[1])]
            if arl[2] in obj.__class__.__dict__.keys():
                valtype = type(obj.__class__.__dict__[arl[2]])
                obj.__dict__[arl[2]] = valtype(arl[3])
            else:
                obj.__dict__[arl[2]] = arl[3]
        elif type(eval(arl[2])) == dict:
            obj = dictionary_obj["{}.{}".format(arl[0], arl[1])]
            for a, b in eval(arl[2]).items():
                if (a in obj.__class__.__dict__.keys() and
                        type(obj.__class__.__dict__[a]) in {str, int, float}):
                    valtype = type(obj.__class__.__dict__[a])
                    obj.__dict__[a] = valtype(b)
                else:
                    obj.__dict__[a] = b
        storage.save()


if __name__ == "__main__":
    HBNBCommand().cmdloop()
