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
