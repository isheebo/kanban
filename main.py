"""
Usage:
    kanban todo <task_name>
    kanban doing <task_id>
    kanban done <task_id>
    kanban edit_task <task_id>
    kanban delete_task <task_id>
    kanban list_todo
    kanban list_doing
    kanban list_done
    kanban list_all

    kanban quit
Options:
  -h --help     Show this screen.
"""

import cmd
import os
from docopt import DocoptExit, docopt
from app.kanban import ToDo


def docopt_cmd(func):
    """
    This decorator simplifies the try/except block and returns
    the result of parsing docopt using an action

    credits: https://github.com/docopt/docopt/blob/master/examples/interactive_example.py
    Contributors: JonLundy, TheWaWaR
    """

    def fn(self, arg):
        try:
            opt = docopt(fn.__doc__, arg)

        except DocoptExit as err:
            # The DocoptExit is thrown when the args do not match
            # We print a message to the user and the usage block
            print('Invalid Command!')
            print(err)
            return

        except SystemExit:
            # The SystemExit exception prints the usage for --help
            # We do not need to do the print here
            return

        return func(self, opt)

    fn.__name__ = func.__name__
    fn.__doc__ = func.__doc__
    fn.__dict__.update(func.__dict__)
    return fn


class Main(cmd.Cmd):
    os.system("cls")
    prompt = "The Kanbanna>>>"

    def __init__(self):
        super().__init__()
        self.kanban = ToDo()

    @docopt_cmd
    def do_todo(self, args):
        """usage: todo <task_name>"""
        task_name = args["<task_name>"]
        description = input("Enter description: ")
        print(self.kanban.todo(task_name, description))

    @docopt_cmd
    def do_doing(self, args):
        """usage: doing <task_id> """
        task_id = args["<task_id>"]
        print(self.kanban.doing(task_id))

    @docopt_cmd
    def do_done(self, args):
        """usage: done <task_id>"""
        task_id = args["<task_id>"]
        print(self.kanban.done(task_id))

    @docopt_cmd
    def do_list_all(self, _):
        """usage: list_all"""
        print(self.kanban.list_all())

    @docopt_cmd
    def do_list_todo(self, _):
        """usage: list_todo"""
        print(self.kanban.list_todo())

    @docopt_cmd
    def do_list_doing(self, _):
        """usage: list_doing"""
        print(self.kanban.list_doing())

    @docopt_cmd
    def do_list_done(self, _):
        """usage: list_done"""
        print(self.kanban.list_done())

    @docopt_cmd
    def do_edit_task(self, args):
        """usage: edit_task <task_id>"""
        task_id = args["<task_id>"]
        print(self.kanban.edit_task(task_id))

    @docopt_cmd
    def do_delete_task(self, args):
        """usage: delete_task <task_id>"""
        task_id = args["<task_id>"]
        print(self.kanban.delete_task(task_id))

    @docopt_cmd
    def do_quit(self, _):
        """quit: exits the application"""
        print('See ya soon!')
        exit(0)


Main().cmdloop()
