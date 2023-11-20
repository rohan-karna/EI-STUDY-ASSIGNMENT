from datetime import datetime
from typing import List

# Task class representing a to-do item
class Task:
    def __init__(self, description: str):
        self.description = description
        self.completed = False
        self.due_date = ""
        self.tags = []
        self.completion_date = None

    def mark_completed(self):
        self.completed = True
        self.completion_date = datetime.now()

    def mark_pending(self):
        self.completed = False
        self.completion_date = None

    def is_completed(self):
        return self.completed

    def get_description(self):
        return self.description

    def get_due_date(self):
        return self.due_date

    def set_due_date(self, date):
        self.due_date = date

    def get_tags(self):
        return self.tags

    def add_tag(self, tag):
        self.tags.append(tag)

    def get_completion_date(self):
        return self.completion_date

# TaskBuilder class for building tasks with optional attributes
class TaskBuilder:
    def __init__(self, description):
        self.task = Task(description)

    def set_due_date(self, due_date):
        self.task.set_due_date(due_date)
        return self

    def add_tag(self, tag):
        self.task.add_tag(tag)
        return self

    def build(self):
        return self.task

# TaskManager class for managing tasks and supporting undo and redo
class TaskManager:
    def __init__(self):
        self.tasks = []
        self.undo_stack = [self.tasks.copy()]
        self.redo_stack = []

    def add_task(self, task):
        self.tasks.append(task)
        self.undo_stack.append(self.tasks.copy())
        self.redo_stack = []

    def mark_completed(self):
        if not self.tasks:
            print("No tasks to mark as completed. Task list is empty.")
            return

        self.display_numbered_tasks()
        task_number = int(input("Enter the task number to mark as completed: ")) - 1

        if 0 <= task_number < len(self.tasks):
            description = self.tasks[task_number].get_description()
            self.tasks[task_number].mark_completed()
            self.undo_stack.append(self.tasks.copy())
            self.redo_stack = []
            print(f"Task '{description}' marked as completed successfully!")
        else:
            print("Invalid task number. No task marked as completed.")

    def delete_task(self):
        if not self.tasks:
            print("No tasks to delete. Task list is empty.")
            return

        self.display_numbered_tasks()
        task_number = int(input("Enter the task number to delete: ")) - 1

        if 0 <= task_number < len(self.tasks):
            description = self.tasks[task_number].get_description()
            del self.tasks[task_number]
            self.undo_stack.append(self.tasks.copy())
            self.redo_stack = []
            print(f"Task '{description}' deleted successfully!")
        else:
            print("Invalid task number. No task deleted.")

    def undo(self):
        if len(self.undo_stack) > 1:
            self.redo_stack.append(self.undo_stack[-1])
            self.undo_stack.pop()
            self.tasks = self.undo_stack[-1]
            print("Undo successful!")
        else:
            print("Undo not possible. No previous state.")

    def redo(self):
        if self.redo_stack:
            self.undo_stack.append(self.redo_stack[-1])
            self.redo_stack.pop()
            self.tasks = self.undo_stack[-1]
            print("Redo successful!")
        else:
            print("Redo not possible. No next state.")

    def view_tasks(self, filter_option="Show all"):
        print("Task List:")
        if not self.tasks:
            print("EMPTY")
        else:
            for task in self.tasks:
                if (filter_option == "Show completed" and task.is_completed()) or \
                        (filter_option == "Show pending" and not task.is_completed()) or \
                        filter_option == "Show all":
                    print(f"{task.get_description()} - {'Completed' if task.is_completed() else 'Pending'}",
                          end="")
                    if task.get_due_date():
                        print(f", Due: {task.get_due_date()}", end="")
                    if task.is_completed():
                        print(f", Completed On: {task.get_completion_date()}", end="")
                    tags = task.get_tags()
                    if tags:
                        print(f", Tags: {' '.join(tags)}", end="")
                    print()

        input("\nPress any key to continue...")

    def display_numbered_tasks(self):
        for i, task in enumerate(self.tasks, start=1):
            print(f"{i}. {task.get_description()}")

# Function to display the menu
def display_menu():
    print("\n===== TO-DO LIST MANAGER =====")
    print("1. Add Task")
    print("2. Mark Task as Completed")
    print("3. Delete Task")
    print("4. Undo")
    print("5. Redo")
    print("6. View Tasks")
    print("0. Exit")
    print("==============================\n")
    print("Enter your choice: ")

def main():
    task_manager = TaskManager()

    while True:
        display_menu()
        choice = input()

        if choice == "1":
            description = input("Enter task description: ")
            due_date = input("Enter due date (or leave empty): ")
            new_task = TaskBuilder(description).set_due_date(due_date).build()
            task_manager.add_task(new_task)
            print("Task added successfully!")

        elif choice == "2":
            task_manager.mark_completed()

        elif choice == "3":
            task_manager.delete_task()

        elif choice == "4":
            task_manager.undo()

        elif choice == "5":
            task_manager.redo()

        elif choice == "6":
            filter_option = input("Select filter option:\n1. Show all\n2. Show completed\n3. Show pending\nEnter your choice: ")
            if filter_option == "1":
                task_manager.view_tasks("Show all")
            elif filter_option == "2":
                task_manager.view_tasks("Show completed")
            elif filter_option == "3":
                task_manager.view_tasks("Show pending")
            else:
                print("Invalid choice!")

        elif choice == "0":
            print("Exiting the program. Goodbye!")
            break

        else:
            print("Invalid choice! Please enter a number between 0 and 6.")

if __name__ == "__main__":
    main()
