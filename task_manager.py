import hashlib
import os


def show_menu():
    while True:
        print("\nMenu:")
        print("1. Register")
        print("2. Login")
        print("3. Exit")

        choice = input("Enter your choice (1-3): ")

        match choice:
            case "1":
                register()
            case "2":
                login()
            case "3":
                print("Exiting the menu")
                exit()
            case _:
                print("Invalid choice. Please try again.")


def register():
    username = input("Enter a username: ")
    password = input("Enter a password: ")

    if is_username_unique(username):
        hashed_password = hash_password(password)
        with open("users.txt", "a") as file:
            file.write(f"{username}:{hashed_password}\n")
        print("Registration successful!")
    else:
        print("Username already exists. Please choose a different username.")


def login():
    username = input("Enter your username: ")
    password = input("Enter your password: ")

    if validate_credentials(username, password):
        print("Login successful!")
        show_task_menu(username)
    else:
        print("Invalid username or password.")


def is_username_unique(username):
    if not os.path.exists("users.txt"):
        return True

    with open("users.txt", "r") as file:
        for line in file:
            if line.startswith(username + ":"):
                return False
    return True


def hash_password(password):
    return hashlib.sha256(password.encode()).hexdigest()


def validate_credentials(username, password):
    if not os.path.exists("users.txt"):
        return False

    with open("users.txt", "r") as file:
        for line in file:
            stored_username, stored_password = line.strip().split(":")
            if username == stored_username and hash_password(password) == stored_password:
                return True
    return False


def show_task_menu(username):
    while True:
        print("\nTask Menu:")
        print("1. Add a Task")
        print("2. View Tasks")
        print("3. Mark a Task as Completed")
        print("4. Delete a Task")
        print("5. Logout")

        choice = input("Enter your choice (1-5): ")

        match choice:
            case "1":
                add_task(username)
            case "2":
                view_tasks(username)
            case "3":
                mark_task_completed(username)
            case "4":
                delete_task(username)
            case "5":
                print("Logged out.")
                break
            case _:
                print("Invalid choice. Please try again.")


def add_task(username):
    description = input("Enter the task description: ")
    task_id = generate_task_id(username)
    status = "Pending"

    with open(username + "_tasks.txt", "a+") as file:
        file.write(f"{task_id}:{description}:{status}\n")

    print("Task added successfully.")


def generate_task_id(username):
    try:
        with open(username + "_tasks.txt", "r") as file:
            lines = file.read().splitlines()
            last_line = lines[-1]
            task_count = int(last_line[0])
    except:
        task_count = 0

    return str(task_count + 1)


def view_tasks(username):
    try:
        with open(username + "_tasks.txt", "r") as file:
            tasks = file.readlines()

        if tasks:
            print("Tasks:")
            for task in tasks:
                task_id, description, status = task.strip().split(":")
                print(f"Task ID: {task_id}")
                print(f"Description: {description}")
                print(f"Status: {status}")
                print()
        else:
            print("No tasks found.")
    except:
        print("No tasks found.")


def mark_task_completed(username):
    try:
        with open(username + "_tasks.txt", "r") as file:
            tasks = file.readlines()

        task_id = input("Enter the task ID to mark as completed: ")

        found = False
        with open(username + "_tasks.txt", "w") as file:
            for task in tasks:
                current_task_id, description, status = task.strip().split(":")
                if current_task_id == task_id:
                    file.write(f"{current_task_id}:{description}:Completed\n")
                    found = True
                else:
                    file.write(task)

        if found:
            print("Task marked as completed.")
        else:
            print("Task not found.")
    except:
        print("No tasks found.")


def delete_task(username):
    try:
        with open(username + "_tasks.txt", "r") as file:
            tasks = file.readlines()

        task_id = input("Enter the task ID to delete: ")

        found = False
        with open(username + "_tasks.txt", "w") as file:
            for task in tasks:
                current_task_id, description, status = task.strip().split(":")
                if current_task_id == task_id:
                    found = True
                else:
                    file.write(task)

        if found:
            print("Task deleted.")
        else:
            print("Task not found.")
    except:
        print("No tasks found.")


show_menu()
