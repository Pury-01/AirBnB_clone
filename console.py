#!/usr/bin/python3
"""The entry point of the command line."""


import shlex
import cmd
from models.base_model import BaseModel
from models import storage


class HBNBCommand(cmd.Cmd):
    prompt = "(hbnb)"

    def do_quit(self, line):
        """Quit command to exit the program"""
        return True

    def help_quit(self):
        """Prints help message for the quit command."""

        print("Quit command to exit the program\n")

    def do_EOF(self, line):
        """when an EOF is met it goes to a new line """
        print()
        return True

    def emptyline(self):
        """Don't execute anything on empty line"""

        pass

    def do_create(self, arg):
        """creates a new instance of BaseModel.
        saves it and prints id.
        """

        if not arg:
            print("** class name missing **")
            return

        # split argument
        args = shlex.split(arg)
        if len(args) == 0:
            return

        class_name = args[0]

        if class_name not in globals():
            print("** class doesn't exist **")
            return

        # dynamically get the class from the global
        classes = globals()[class_name]

        # create new instance of the class
        try:
            new_instance = classes()
            new_instance.save()
            print(new_instance.id)
        except Exception as e:
            print("Error creating instance: {e}")

    def do_show(self, arg):
        """prints the string representation of an instance.
        it is based on the class name and id."""

        if not arg:
            print("** class name missing **")
            return

        args = shlex.split(arg)

        if len(args) < 2:
            print("** instance id missing **")
            return

        class_name = args[0]
        obj_id = args[1]

        if class_name not in globals():
            print("** class doesn't exist **")
            return

        key = class_name + "." + obj_id
        objects = storage.all()
        obj = objects.get(key)

        if obj:
            print(obj)
        else:
            print(" ** no instance found **")

    def do_destroy(self, arg):
        """deletes an instance based on class name and id.
        saves changes into the JSON file."""

        args = shlex.split(arg)

        if not args:
            print("** class name missing **")
            return

        if len(args) < 2:
            print("** instance id missing **")
            return
        
        class_name = args[0]
        obj_id = args[1]

        key = f"{class_name}.{obj_id}"
        all_objects = storage.all()

        if key in all_objects:
            del all_objects[key]
            storage.save()
        else:
            print("** no instance found **")

    def do_all(self, arg):
        """prints all string representation of all instances.
        it is based or not on the class name."""

        args = shlex.split(arg)
        all_objects = storage.all()
        obj_list = []

        if not args:
            for obj in all_objects.values():
                obj_list.append(str(obj))
        else:
            class_name = args[0]
            if class_name not in globals():
                print("** class doesn't exist **")
                return
        
            for key, obj in all_objects.items():
                if key.split('.')[0] == class_name:
                    obj_list.append(str(obj))
        print(obj_list)

    def do_update(self, arg):
        """updates an instance based on the class name ans id.
        this is by adding or updating attribute."""

        pass


if __name__ == '__main__':
    HBNBCommand().cmdloop()
