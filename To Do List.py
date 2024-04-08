import os
import json
import datetime
from colorama import init, Fore, Back, Style

init(autoreset=True)

def clear_screen(): 
    if os.name == 'nt': 
        os.system('cls') 
    else:
        os.system('clear')  

class TaskManager:
    def __init__(self):
        self.tasks = self.load_tasks()

    def load_tasks(self):
        try:
            with open('tasks.json', 'r') as file:
                return json.load(file)
        except FileNotFoundError:
            return []

    def save_tasks(self):
        try:
            with open('tasks.json' , 'w') as file:
                json.dump(self.tasks,file)
        except IOError as e:
            print(Fore.RED + f"Error saving tasks: {e}")
        except Exception as e: 
            print(Fore.RED + f"An unexpected error occurred: {e}")

    def show_tasks(self):
        priority_mapping = {"High": 1, "Medium": 2, "Low": 3}
        if not self.tasks:  
            print(Fore.YELLOW + "No tasks to show.")
        else:
            print("To-Do List:")
            sorted_tasks = sorted(self.tasks, key=lambda x: priority_mapping.get(x.get("priority", "Low"), 3))
            for index, task in enumerate(self.tasks, start=1):
                status = "Done" if task["completed"] else "Not Done"
                due_date = task.get("due_date", "No due date")
                priority = task.get("priority", "No priority")
                print(f"{index}. {task['description']} - {status} - Due: {due_date}")

    def add_task(self):
        description = input("Enter task description")
        due_date = input("Enter due date (MM-DD-YYYY: )")
        priority = input("Enter task priority (High, Medium, Low): ")
        self.tasks.append({"description": description, "completed": False, "due_date": due_date, "priority": priority})
        print(Fore.GREEN + "Task added.")
        self.save_tasks()

    def delete_task(self, task_number):
        if 0 < task_number <= len(self.tasks):
            del self.tasks[task_number - 1]
            print (Fore.RED + "Task deleted.")
        else:
            print(Fore.RED + "Invalid task number.")
        self.save_tasks()

    def complete_task(self, task_number):
        if 0 < task_number <= len(self.tasks):
            self.tasks[task_number - 1]["completed"] = True
            print(Fore.GREEN + "Task marked as completed.")
        else:
            print(Fore.RED + "Invalid task number.")
        self.save_tasks()

    def edit_task(self, task_number, new_description=None, new_due_date=None, new_priority=None):
        if 0 < task_number <= len(self.tasks):
            if new_description:
                self.tasks[task_number - 1]['description'] = new_description
            if new_due_date: 
                self.tasks[task_number - 1]['due_date'] = new_due_date
            if new_priority:
                self.tasks[task_number - 1]['priority'] = new_priority
            print(Fore.GREEN + "Task updated successfully.")
            self.save_tasks() 
        else:
            print(Fore.RED + "Invalid task number.")
    
    def check_reminders(self):
        current_date = datetime.date.today()
        for task in self.tasks:
            try:
                task_due_date = datetime.datetime.strptime(task["due_date"], '%m-%d-%Y').date()
                if (task_due_date - current_date).days <= 1: 
                    print(Fore.YELLOW + f'Reminder: The task "{task["description"]}" is due soon on {task["due_date"]}.')
            except ValueError:
                print(Fore.RED + f'Error: Incorrect date format for task "{task["description"]}". Please use MM-DD-YYYY.')

                continue
        

def show_menu():
    clear_screen()
    print("1. Show all tasks")
    print("2. Add a new task")
    print("3. Delete a task")
    print("4. Mark a task as completed")
    print("5. Edit a task description")
    print("6. Exit")

def main():
    task_manager = TaskManager()
    while True:
        show_menu()
        task_manager.check_reminders()  
        choice = input("Choose an option: ")
        if choice == "1":
            task_manager.show_tasks()
        elif choice == "2": 
            task_manager.add_task()
        elif choice == "3":
            task_number = int(input("Enter task number to delete: "))
            task_manager.delete_task(task_number)
        elif choice == "4":
            task_number = int(input("Enter task number to mark as completed: "))
            task_manager.complete_task(task_number)
        elif choice == "5":
            task_number = int(input("Enter task number to edit: "))
            new_description = input("Enter new task description (leave blank to keep current): ")
            new_due_date = input("Enter a new due date (MM-DD-YYYY) (leave blank to keep current): ")
            new_priority = input("Enter new priority (High, Medium, Low) (leave blanks to keep current): ")
            task_manager.edit_task(task_number, new_description if new_description else None, new_due_date if new_due_date else None, new_priority if new_priority else None)
        elif choice == "6":
            print("Goodbye!")
            break
        else:
            print(Fore.RED + "Invalid choice. Please choose a valid option.")
        input("Press Enter to return to the menu...") 
        clear_screen()

if __name__== "__main__":
    main()
