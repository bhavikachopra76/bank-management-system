import json
from pathlib import Path
import random
import string
from datetime import datetime

class Expense:

    database = 'expense.json'
    data = []

    try:
        if Path(database).exists():
            with open(database) as fs:
                data = json.load(fs)
        else:
            print("Database does not exist")
    except Exception as e:
        print(e)


    @staticmethod
    def __update():
        with open(Expense.database , 'w') as fs:
            json.dump(Expense.data , fs)

    @staticmethod
    def generate_user():
        alpha = random.choices(string.ascii_letters , k=6)
        num = random.choices(string.digits, k=4)
        spchar = random.choices("@#$&" , k = 1)
        user_id = alpha + num + spchar
        random.shuffle(user_id)
        return "".join(user_id)

    @staticmethod
    def create_account():
        info = {
            "name" : input("Enter your name: "),
            "email" : input("Enter your email: ").lower(),
            "password" : input("Enter your password: "),
            "userID" : Expense.generate_user(),
            "expenses": []
        }
        user_info = [x for x in Expense.data if x['email'] == info['email']]
        if not user_info:
            Expense.data.append(info)
            Expense.__update()
            print(f"Account created successfully \nUser Id : {info['userID']} ")
        else:
            print(f"Account already exists.")

    @staticmethod
    def login_account():
        userId = input("Enter your user ID: ")
        pwd = input("Enter your password: ")
        user_info = [x for x in Expense.data if x['userID'] == userId and x['password'] == pwd ]
        if not user_info:
            print("Invalid userID or password")
            return None
        else:
            print(f"Welcome Back! {user_info[0]['name']}")
            return user_info[0]

    @staticmethod
    def add_expense(logged_in_user):
        try:
            amount = int(input("Enter your expense amount: "))
            if amount <= 0:
                print("Amount must be greater than 0")
                return
        except ValueError:
            print("Invalid amount entered")
            return

        date_input = input("Enter your expense date (DD-MM-YYYY) or press Enter for today: ").strip()

        if date_input == "":
            date = datetime.now().strftime("%d-%m-%Y")
        else:
            date = date_input

        new_expense = {
            "amount": amount,
            "category": input("Enter your expense category: "),
            "date": date,
            "note": input("Enter your expense note: "),
        }

        logged_in_user['expenses'].append(new_expense)
        Expense.__update()
        print("Expense added successfully!")


    @staticmethod
    def update_expense(logged_in_user):
        date = input("Enter your expense date (DD-MM-YYYY): ").strip()
        cat = input("Enter your expense category: ").strip()
        matched = [x for x in logged_in_user['expenses'] if x['date'] == date and x['category'] == cat]
        if not matched:
            print("No expenses found")

        for i, exp in enumerate(matched , 1):
            print(f"{i} | {exp['date']} | {exp['category']} | ₹{exp['amount']} | {exp['note']}")

        if len(matched) > 1:
            choice = int(input("Enter your choice: "))
            selected = matched[choice]
        else:
            selected = matched[0]

        new_amount = input("Enter new amount or press enter to skip: ").strip()
        new_category = input("Enter new category or press enter to skip: ").strip()
        new_note = input("Enter new note or press enter to skip: ").strip()
        new_date = input("Enter new date or press enter to skip: ").strip()

        if new_amount: selected['amount'] = int(new_amount)
        if new_category: selected['category'] = new_category
        if new_date: selected['date'] = new_date
        if new_note: selected['note'] = new_note

        Expense.__update()
        print("Expense updated successfully!")

    @staticmethod
    def delete_expense(logged_in_user):
        date = input("Enter your expense date (DD-MM-YYYY): ").strip()
        cat = input("Enter your expense category: ").strip()

        matched = [
            x for x in logged_in_user['expenses']
            if x['date'] == date and x['category'].lower() == cat.lower()
        ]

        if not matched:
            print("No expenses found")
            return

        for i, exp in enumerate(matched, 1):
            print(f"{i} | {exp['date']} | {exp['category']} | ₹{exp['amount']} | {exp['note']}")

        if len(matched) > 1:
            choice = int(input("Enter your choice: "))
            selected = matched[choice - 1]
        else:
            selected = matched[0]

        logged_in_user['expenses'].remove(selected)
        Expense.__update()

        print("Expense deleted successfully!")

    @staticmethod
    def view_expense(logged_in_user):
        exp = logged_in_user['expenses']
        if not exp:
            print("No expenses found")
            return
        exp.sort(key=lambda x: datetime.strptime(x['date'], "%d-%m-%Y"))
        print("📋 Your Expenses:")
        for expense in exp:
            print(f"{expense['date']} | {expense['category']} | {expense['amount']} | {expense['note']}")
        total = 0
        for expense in exp:
            total += expense['amount']
        print(f"\nTotal Expenses : {total}")


    def set_budget(self, logged_in_user):
        pass


    def show_budget(self , logged_in_user):
        pass

    def show_summary(self , logged_in_user):
        pass


user = Expense()
print("Press 1 to Register")
print("Press 2 to Login")
check = int(input("Enter your choice: "))
if check == 1:
    user.create_account()
if check == 2:
    logged_in = user.login_account()
    if logged_in:
        print("Press 1 to Add Expense")
        print("Press 2 to Update Expense")
        print("Press 3 to Delete Expense")
        print("Press 4 to View all Expenses")
        print("Press 5 to Set Budget per category")
        print("Press 6 to View Budget Status")
        print("Press 7 to Show Monthly report")
        action = int(input("Enter your choice: "))
        if action == 1:
            user.add_expense(logged_in)
        if action == 2:
            user.update_expense(logged_in)
        if action == 3:
            user.delete_expense(logged_in)
        if action == 4:
            user.view_expense(logged_in)
        if action == 5:
            user.set_budget(logged_in)
        if action == 6:
            user.show_budget(logged_in)
        if action == 7:
            user.show_summary(logged_in)