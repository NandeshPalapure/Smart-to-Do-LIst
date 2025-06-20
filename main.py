import json
from datetime import datetime, date, timedelta
import os

TASKS_FILE = 'tasks.json'

# Load tasks from file
def load_tasks():
    if not os.path.exists(TASKS_FILE):
        return []
    with open(TASKS_FILE, 'r') as file:
        return json.load(file)

# Save tasks to file
def save_tasks(tasks):
    with open(TASKS_FILE, 'w') as file:
        json.dump(tasks, file, indent=4)

# Automatically mark overdue tasks
def update_overdue(tasks):
    today = date.today()
    for task in tasks:
        if task['Status'] == 'Pending':
            due_date = datetime.strptime(task['Due Date'], "%Y-%m-%d").date()
            if due_date < today:
                task['Status'] = 'Overdue'
    return tasks

# Add Task
def add_task():
    tasks = load_tasks()
    title = input("Enter Task Title: ")
    description = input("Enter Task Description: ")
    due_date = input("Enter Due Date (YYYY-MM-DD): ")
    priority = input("Enter Priority (High/Medium/Low): ").capitalize()
    task_id = tasks[-1]['ID'] + 1 if tasks else 1
    created_at = datetime.now().strftime("%Y-%m-%d %H:%M:%S")

    task = {
        'ID': task_id,
        'Title': title,
        'Description': description,
        'Due Date': due_date,
        'Priority': priority,
        'Status': 'Pending',
        'Created At': created_at,
        'Completed At': ""
    }
    tasks.append(task)
    save_tasks(tasks)
    print("Task added successfully!")

# Mark Task as Completed
def mark_completed():
    tasks = load_tasks()
    task_id = int(input("Enter Task ID to mark as completed: "))
    for task in tasks:
        if task['ID'] == task_id:
            if task['Status'] != 'Completed':
                task['Status'] = 'Completed'
                task['Completed At'] = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                print("Task marked as Completed.")
            else:
                print("Task is already marked as Completed.")
            break
    else:
        print("Task ID not found.")
    save_tasks(tasks)

# Delete Task
def delete_task():
    tasks = load_tasks()
    task_id = int(input("Enter Task ID to delete: "))
    tasks = [task for task in tasks if task['ID'] != task_id]
    save_tasks(tasks)
    print("Task deleted successfully!")

# View All Tasks (Color + Sorting)
def view_tasks():
    tasks = load_tasks()
    tasks = update_overdue(tasks)
    if not tasks:
        print("No tasks found.")
        return

    priority_order = {"High": 1, "Medium": 2, "Low": 3}
    tasks.sort(key=lambda x: (x['Status'] != 'Overdue', priority_order.get(x['Priority'], 4)))

    print("\n===== All Tasks =====")
    for task in tasks:
        # Color coding
        if task['Priority'] == 'High':
            color = '\033[91m' 
        elif task['Priority'] == 'Medium':
            color = '\033[93m'  
        elif task['Priority'] == 'Low':
            color = '\033[92m'
        else:
            color = '\033[0m'   

        if task['Status'] == 'Overdue':
            color = '\033[95m' 
            
        print(f"{color}ID: {task['ID']}, Title: {task['Title']}, Due: {task['Due Date']}, Priority: {task['Priority']}, Status: {task['Status']}\033[0m")

# Filter Tasks
def filter_tasks():
    tasks = load_tasks()
    tasks = update_overdue(tasks)
    print("Filter Options:\n1. Pending\n2. Completed\n3. Due Today\n4. Due Tomorrow\n5. Overdue")
    choice = input("Enter your filter choice (1-5): ")

    today = date.today()
    tomorrow = today + timedelta(days=1)

    if choice == '1':
        filtered = [t for t in tasks if t['Status'] == 'Pending']
    elif choice == '2':
        filtered = [t for t in tasks if t['Status'] == 'Completed']
    elif choice == '3':
        filtered = [t for t in tasks if datetime.strptime(t['Due Date'], "%Y-%m-%d").date() == today]
    elif choice == '4':
        filtered = [t for t in tasks if datetime.strptime(t['Due Date'], "%Y-%m-%d").date() == tomorrow]
    elif choice == '5':
        filtered = [t for t in tasks if t['Status'] == 'Overdue']
    else:
        print("Invalid choice.")
        return

    if not filtered:
        print("No tasks found for this filter.")
    else:
        for task in filtered:
            print(f"ID: {task['ID']}, Title: {task['Title']}, Due: {task['Due Date']}, Priority: {task['Priority']}, Status: {task['Status']}")

# Search Tasks by Keyword
def search_tasks():
    tasks = load_tasks()
    keyword = input("Enter keyword to search in Title or Description: ").lower()
    found = False

    print("\n===== Search Results =====")
    for task in tasks:
        if keyword in task['Title'].lower() or keyword in task['Description'].lower():
            found = True
            print(f"ID: {task['ID']}, Title: {task['Title']}, Due: {task['Due Date']}, Priority: {task['Priority']}, Status: {task['Status']}")
    
    if not found:
        print("No matching tasks found.")

# Main Menu
def main():
    while True:
        print("\n====== Smart To-Do List Manager ======")
        print("1. Add Task")
        print("2. Mark Task as Completed")
        print("3. Delete Task")
        print("4. View All Tasks")
        print("5. Filter Tasks")
        print("6. Search Tasks")
        print("7. Exit")

        choice = input("Enter your choice (1-7): ")

        if choice == '1':
            add_task()
        elif choice == '2':
            mark_completed()
        elif choice == '3':
            delete_task()
        elif choice == '4':
            view_tasks()
        elif choice == '5':
            filter_tasks()
        elif choice == '6':
            search_tasks()
        elif choice == '7':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please try again.")

if __name__ == "__main__":
    main()
