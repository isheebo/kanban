import sqlite3
import os
from datetime import datetime
import tabulate


def connect(filename):
    is_existing = os.path.exists(filename)
    db = sqlite3.connect("kanban.db")
    cursor = db.cursor()
    if not is_existing:
        cursor.execute("CREATE TABLE Task ("
                       "ID INTEGER PRIMARY KEY AUTOINCREMENT,"
                       "Name TEXT NOT NULL,"
                       "Description TEXT NOT NULL,"
                       "Status TEXT NOT NULL,"
                       "Start DATETIME,"
                       "Finish DATETIME,"
                       "Duration DATETIME);"
                       )
    return db


class ToDo:
    """ ToDo """

    def __init__(self):
        self.db = connect("kanban.db")
        self.cursor = self.db.cursor()

    def todo(self, task_name, task_description):
        self.cursor.execute("INSERT INTO Task(Name, Description, Status)VALUES(?,?,?)",
                            (task_name, task_description, "ToDo"))
        self.db.commit()
        return f"A task with name '{task_name.title()}' has been created successfully!"

    def doing(self, task_id):
        """ We can only  mark a status as 'doing' only and only if it was on the todo list. """
        self.cursor.execute(f"SELECT Status FROM Task WHERE ID = {task_id}")
        results = self.cursor.fetchone()
        if results:
            status = results[0]
            if status == "ToDo":
                try:
                    self.cursor.execute("UPDATE Task SET Status ='Doing',Start='{0}' WHERE ID = {1}".format(
                        datetime.now().strftime("%Y-%m-%d %H:%M:%S"), task_id))
                    self.db.commit()
                    return f"Task with ID {task_id} has been successfully updated!"
                except sqlite3.OperationalError:
                    print("Your task ID doesn't exist!")

            elif status == "Doing":
                return "You are already doing this task"

            elif status == "Done":
                # if task exists and has been marked as done, we can change it's
                # status to doing directly to reduce on data duplication within
                # the database
                try:
                    self.cursor.execute(
                        "UPDATE Task SET Status ='Doing',Start='{0}', Finish='NULL' WHERE ID = {1}".format(
                            datetime.now().strftime("%Y-%m-%d %H:%M:%S"), task_id))
                    self.db.commit()
                    return f"Task with ID {task_id} has been successfully updated!"
                except sqlite3.OperationalError as err:
                    return f"{err}"
            return "Unknown task status: status can only be done, todo or doing"
        return "Task with the specified ID doesn't exist.. please try listing the tasks and try again"

    def done(self, task_id):
        """ We can only check a task as done.. only and only if we have been doing it.
        i.e: It's past status must be 'doing' """
        self.cursor.execute(f"SELECT Status FROM Task WHERE ID = {task_id}")
        results = self.cursor.fetchone()
        if results:
            status = results[0]
            if status == "Doing":
                try:
                    self.cursor.execute(
                        f"SELECT Start FROM Task WHERE ID={task_id}")
                    start_time = datetime.strptime(
                        self.cursor.fetchone()[0], "%Y-%m-%d %H:%M:%S")
                    finish_time = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    duration = datetime.strptime(
                        finish_time, "%Y-%m-%d %H:%M:%S") - start_time
                    self.cursor.execute(
                        "UPDATE Task SET Status='Done', Finish='{0}', Duration='{1}'  WHERE ID = {2}".format(
                            finish_time, duration, task_id))
                    self.db.commit()
                    return f"Task with ID {task_id} has successfully been completed!"
                except sqlite3.OperationalError:
                    return "unknown task ID"
            if status == "Done":
                return "Task has already been completed"
            return "The task specified is still on the todo list: try changing it's status first"
        return "unknown task ID: try listing the tasks first so as to select the appropriate ID"

    def list_all(self):
        self.cursor.execute("SELECT ID, Name, Description, Status FROM Task")
        results = self.cursor.fetchall()
        if results:
            headers = ["ID", "Name", "Description", "Status"]
            return tabulate.tabulate(results, headers, tablefmt="fancy_grid")
        return "No tasks added yet! please add some tasks and try again"

    def list_todo(self):
        self.cursor.execute(
            "SELECT ID, Name, Description FROM Task WHERE Status='ToDo'")
        results = self.cursor.fetchall()
        if results:
            headers = ["ID", "Name", "Description"]
            return tabulate.tabulate(results, headers, tablefmt="fancy_grid")
        return "You currently have no pending (to do) tasks"

    def list_doing(self):
        self.cursor.execute(
            "SELECT ID, Name, Description, Start FROM Task WHERE Status='Doing'")
        results = self.cursor.fetchall()
        if results:
            headers = ["ID", "Name", "Description", "Start Time"]
            return tabulate.tabulate(results, headers, tablefmt="fancy_grid")
        return "No tasks are being worked on currently!"
