import csv
from datetime import datetime

expenses = []
monthly_budget = 0.0


def add_expense():
    date = input("Enter the date of the expense (YYYY-MM-DD): ")
    category = input(
        "Enter the category of the expense (e.g., Food, Travel): ")
    amount = float(input("Enter the amount spent: "))
    description = input("Enter a brief description of the expense: ")

    expense = {
        'date': date,
        'category': category,
        'amount': amount,
        'description': description
    }
    expenses.append(expense)
    print("Expense added successfully.")


def view_expenses():
    if not expenses:
        print("No expenses recorded.")
        return

    print("\n--- Expense List ---")
    for expense in expenses:
        if all(k in expense and expense[k] for k in ['date', 'category', 'amount', 'description']):
            print(f"Date: {expense['date']}, Category: {expense['category']}, "
                  f"Amount: {expense['amount']}, Description: {expense['description']}")
        else:
            print("Incomplete expense entry found, skipping...")
    print("\n--- End of Expenses ---")


def set_budget():
    global monthly_budget
    monthly_budget = float(input("Enter your monthly budget amount: "))
    print(f"Budget set to {monthly_budget}.")


def track_budget():
    total_expenses = sum(expense['amount'] for expense in expenses)
    remaining_budget = monthly_budget - total_expenses
    print(f"\nTotal expenses: {total_expenses}")

    if total_expenses > monthly_budget:
        print("Warning: You have exceeded your budget!")
    else:
        print(f"You have {remaining_budget} left for the month.")


def save_expenses():
    with open('expenses.csv', 'w', newline='') as file:
        writer = csv.writer(file)
        writer.writerow(['date', 'category', 'amount', 'description'])
        for expense in expenses:
            writer.writerow([expense['date'], expense['category'],
                            expense['amount'], expense['description']])
    print("Expenses saved to 'expenses.csv'.")


def load_expenses():
    try:
        with open('expenses.csv', 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                row['amount'] = float(row['amount'])
                expenses.append(row)
        print("Expenses loaded successfully.")
    except FileNotFoundError:
        print("No previous expenses found.")


def display_menu():
    while True:
        print("\n--- Expense Tracker Menu ---")
        print("1. Add expense")
        print("2. View expenses")
        print("3. Track budget")
        print("4. Save expenses")
        print("5. Exit")

        choice = input("Choose an option: ")

        match choice:
            case '1':
                add_expense()
            case '2':
                view_expenses()
            case '3':
                if monthly_budget == 0:
                    set_budget()
                track_budget()
            case '4':
                save_expenses()
            case '5':
                save_expenses()
                print("Exiting the program.")
                break
            case _:
                print("Invalid choice. Please try again.")


load_expenses()

display_menu()
