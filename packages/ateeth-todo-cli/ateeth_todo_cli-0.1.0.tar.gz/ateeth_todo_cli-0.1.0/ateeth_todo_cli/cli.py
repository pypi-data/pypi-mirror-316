import datetime
from typing import Optional
import typer
from ateeth_todo_cli.model.Task import Task
import json
import os
import pandas as pd

app = typer.Typer()

file_path = "ateeth_todo_cli/data/tasks.json"
key = "tasks"

def file_exist_check():
    if not os.path.exists(file_path):
        print("Creating file")
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as file:
            json.dump({key: []}, file)
    
def read_tasks() :
    task_list = []
    try:
        with open(file_path, 'r') as file:
            data = json.load(file)
            task_list = data.get(key, [])
    except (json.JSONDecodeError, IOError) as e:
        print(f"Error reading or parsing {file_path}: {e}. Returning an empty list.")
    
    return task_list

def write_tasks(task_list):
    with open(file_path, 'w') as file:
        json.dump({key: task_list}, file, indent=4)
            
@app.command()
def add(task: str):
    """
    Add a new task to the todo list.
    """
    file_exist_check()
    tasks = read_tasks()
    newTask = Task(task, len(tasks) + 1)
    newTask_dict = newTask.to_dict()
    tasks.append(newTask_dict)
    write_tasks(tasks)
    print(f"Task added successfully (ID: {newTask_dict['id']})")

@app.command()
def list(query: Optional[str] = typer.Argument(None)):
    """
    List all tasks in the todo list.
    
    A query can be passed optionally such as 
        done: To list the tasks which have status done
        in-progress: To list the tasks which have status in-progress
    """
    file_exist_check()
    tasks = read_tasks()
    
    if query:
        filtered_tasks = [task for task in tasks if task["status"].lower() == query.lower()]
        if not filtered_tasks:
            typer.echo(f"No tasks found with status: {query}")
            return
    else:
        filtered_tasks = tasks
        
    df = pd.DataFrame(filtered_tasks)
    print(df)

@app.command()
def update(id: int, desc: str):
    """
    Update the description of a specific task
    Args:
        id (int): id of the task whose description is to be updated
        desc (str): updated description
    """
    file_exist_check()
    tasks = read_tasks()    
    for i in range(len(tasks)):
        if tasks[i]["id"] == id :
            tasks[i]["description"] = desc
            tasks[i]["updatedAt"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            write_tasks(tasks)
            typer.echo(f"Task {id} is updated")
            return
            
    typer.echo(f"Task with {id} not found !!")

@app.command()
def delete(id: int) :
    """
    Delete a specifc task
    Args:
        id (int): id of task to be deleted
    """
    file_exist_check()
    tasks = read_tasks()
    
    for i in range(len(tasks)):
        if tasks[i]["id"] == id :
            tasks.pop(i)
            typer.echo(f"Task with id {id} deleted successfully")
            write_tasks(tasks)
            return
    
    typer.echo(f"Task with {id} not found !!")

@app.command()
def mark_in_progress(id : int):
    """
    Change the status of a specific task to in-progress
    Args:
        id (int): id of the task whose status is to be changed to in-progress
    """
    file_exist_check()
    tasks = read_tasks()
    
    for i in range(len(tasks)):
        if tasks[i]["id"] == id :
            tasks[i]["status"] = "in-progress"
            tasks[i]["updatedAt"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            typer.echo(f"Task with id {id} has been updated to in-progress")
            write_tasks(tasks)
            return
    
    typer.echo(f"Task with {id} not found !!")
    
@app.command()
def mark_done(id : int):
    """
    Change the status of a specific task to done
    Args:
        id (int): id of the task whose status is to be changed to done
    """
    file_exist_check()
    tasks = read_tasks()
    
    for i in range(len(tasks)):
        if tasks[i]["id"] == id :
            tasks[i]["status"] = "done"
            tasks[i]["updatedAt"] = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S") 
            typer.echo(f"Task with id {id} has been updated to done")
            write_tasks(tasks)
            return
    
    typer.echo(f"Task with {id} not found !!")

if __name__ == "__main__":
    app()
