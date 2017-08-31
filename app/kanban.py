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
