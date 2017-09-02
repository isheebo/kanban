# Kanban App
This application implements the basic functionality of a ToDo list application. 

Add the tasks to be done using the todo command. Tasks can then be shuffled from todo, to doing and then to done.

## Using
It is assumed that you have [Python 3.6](https://www.python.org) & [git](https://git-scm.com) installed. Grab this sourcecode and run this app by 
```sh 
$ git clone https://github.com/isheebo/kanban.git
$ cd kanban
$ pip install -r requirements.txt
$ python main.py
```
On running the application, type `help` for the list of valid commands. For help on a specific command, type `help <command_name>` e.g. `help delete_task`

## Documentation

- **todo** *task_name* : Adds a task to the todo list
- **doing** *task_id*: Marks the task as currently in progress (being worked on)
- **done** *task_id*: Marks the task as done
- **edit_task** *task_id* : Edits the task specified by ID
- **delete_task** *task_id*:  Deletes task specified by ID

- **list_all**: Lists all the tasks that have been added by the user
- **list_todo**: Lists tasks currently marked as ToDos
- **list_doing**: Lists all tasks that are being worked on
- **list_done**: lists only tasks that have been completed
-  **quit**: Exits the application


## Author
Kanyesigye Edgar