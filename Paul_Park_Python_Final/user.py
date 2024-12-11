
from datetime import datetime
from db import DatabaseManager
from object import BudgetCalculator

class BudgetTrackerApp:
    def __init__(self):
        self.db_manager = DatabaseManager()
        self.calculator = BudgetCalculator(self.db_manager)
        self.db_manager.create_tables()

    def get_valid_input(self, prompt):
        while True:
            user_input = input(prompt).strip()
            if user_input.lower() == "b":
                return "go_back"
            try:
                value = float(user_input)
                if len(user_input.split(".")[-1]) == 2:
                    return value
                else:
                    print("Enter a valid amount with two decimal places (e.g., 32.50).")
            except ValueError:
                print("Invalid input. Enter a numeric amount in dollars ($).")

    def display_menu(self):
        current_date = datetime.now().strftime("%B %Y")
        print(f"\nBudget Tracker Menu - {current_date}")
        print("=" * 40)
        print("1. Add Income")
        print("2. Edit Income")
        print("3. Set Monthly Budget")
        print("4. Edit Budget")
        print("5. Add Expense")
        print("6. Edit Expense")
        print("7. View Budget Status")
        print("8. View Summary")
        print("9. View Savings")
        print("10. Exit")

    def add_income(self):
        source = input("Income source (or type 'B' to go back): ").strip()
        if source.lower() == "b":
            return
        amount = self.get_valid_input("Income amount (or type 'B' to go back): ")
        if amount == "go_back":
            return
        self.db_manager.add_income(source, amount)
        print(f"Income of ${amount:.2f} from {source} added successfully!")

    def edit_income(self):
        incomes = self.db_manager.get_income()
        if not incomes:
            print("No incomes available to edit.")
            return

        print("Select an income to edit (or type 'B' to go back):")
        for i, (income_id, source, amount, month_year) in enumerate(incomes, start=1):
            print(f"{i}. {source} - ${amount:.2f} ({month_year})")
        choice = input("Your choice: ").strip()

        if choice.lower() == "b":
            return

        if choice.isdigit() and 1 <= int(choice) <= len(incomes):
            income_id = incomes[int(choice) - 1][0]
            new_amount = self.get_valid_input("Enter the new amount: ")
            if new_amount == "go_back":
                return
            self.db_manager.update_income(income_id, new_amount)
            print("Income updated successfully!")
        else:
            print("Invalid choice.")

    def set_budget(self):
        total_income = self.calculator.calculate_income()
        categories = ["housing", "food", "utilities", "transportation", "entertainment", "other"]
        print("Enter budgets for the following categories:")
        allocated_budget = 0

        for category in categories:
            print(f"Category: {category.capitalize()}")
            allocated = self.get_valid_input("Enter allocated amount: ")
            if allocated == "go_back":
                return
            if allocated_budget + allocated > total_income:
                print("Error: Budget cannot exceed total income.")
                continue
            self.db_manager.set_category_budget(category, allocated)
            allocated_budget += allocated

        print("Budget set successfully!")

    def edit_budget(self):
        month_year = datetime.now().strftime("%B-%Y")
        budgets = self.db_manager.get_budget_status_for_month(month_year)
        if not budgets:
            print("No budgets available to edit.")
            return

        print("Select a category to edit (or type 'B' to go back):")
        for i, (category, budget, spent) in enumerate(budgets, start=1):
            print(f"{i}. {category.capitalize()} - Budget: ${budget:.2f}, Spent: ${spent:.2f}")
        choice = input("Your choice: ").strip()

        if choice.lower() == "b":
            return

        if choice.isdigit() and 1 <= int(choice) <= len(budgets):
            category = budgets[int(choice) - 1][0]
            new_budget = self.get_valid_input("Enter the new budget: ")
            if new_budget == "go_back":
                return
            self.db_manager.update_budget(category, new_budget)
            print("Budget updated successfully!")
        else:
            print("Invalid choice.")

    def add_expense(self):
        month_year = datetime.now().strftime("%B-%Y")
        budgets = self.db_manager.get_budget_status_for_month(month_year)
        if not budgets:
            print("No budget categories available. Please set a budget first.")
            return

        print("Available categories:")
        for category, budget, spent in budgets:
            print(f"- {category.capitalize()}")

        category = input("Enter category (or type 'B' to go back): ").strip()
        if category.lower() == "b":
            return

        if not any(category.lower() == cat[0].lower() for cat in budgets):
            print("Invalid category. Please try again.")
            return

        amount = self.get_valid_input("Enter expense amount: ")
        if amount == "go_back":
            return
        self.db_manager.add_category_expense(category, amount)
        print(f"Expense of ${amount:.2f} added to {category.capitalize()}!")

    def edit_expense(self):
        month_year = datetime.now().strftime("%B-%Y")
        budgets = self.db_manager.get_budget_status_for_month(month_year)
        if not budgets:
            print("No expenses available to edit.")
            return

        print("Select a category to edit expenses (or type 'B' to go back):")
        for i, (category, budget, spent) in enumerate(budgets, start=1):
            print(f"{i}. {category.capitalize()} - Spent: ${spent:.2f}")
        choice = input("Your choice: ").strip()

        if choice.lower() == "b":
            return

        if choice.isdigit() and 1 <= int(choice) <= len(budgets):
            category = budgets[int(choice) - 1][0]
            new_spent = self.get_valid_input("Enter the new spent amount: ")
            if new_spent == "go_back":
                return
            self.db_manager.update_expense(category, new_spent)
            print("Expense updated successfully!")
        else:
            print("Invalid choice.")

    def view_budget_status(self):
        month_year = datetime.now().strftime("%B-%Y")
        statuses = self.db_manager.get_budget_status_for_month(month_year)
        if not statuses:
            print("No budget data available for the current month.")
            return

        print("\nBudget Status")
        print("=" * 40)
        for category, budget, spent in statuses:
            print(f"{category.capitalize()}: Budget ${budget:.2f}, Spent ${spent:.2f}")
        print("=" * 40)

    def view_summary(self):
        total_expenses = self.calculator.calculate_total_expenses()
        total_income = self.calculator.calculate_income()
        remaining_budget = total_income - total_expenses

        print("\nSummary")
        print("=" * 40)
        print(f"Total Income: ${total_income:.2f}")
        print(f"Total Expenses: ${total_expenses:.2f}")
        print(f"Remaining Budget: ${remaining_budget:.2f}")
        print("=" * 40)

    def view_savings(self):
        total_savings = self.calculator.calculate_savings()
        print("\nSavings")
        print("=" * 40)
        print(f"Total Savings: ${total_savings:.2f}")
        print("=" * 40)

    def run(self):
        while True:
            self.display_menu()
            choice = input("Your choice: ").strip()
            if choice == "1":
                self.add_income()
            elif choice == "2":
                self.edit_income()
            elif choice == "3":
                self.set_budget()
            elif choice == "4":
                self.edit_budget()
            elif choice == "5":
                self.add_expense()
            elif choice == "6":
                self.edit_expense()
            elif choice == "7":
                self.view_budget_status()
            elif choice == "8":
                self.view_summary()
            elif choice == "9":
                self.view_savings()
            elif choice == "10":
                print("Goodbye!")
                break
            else:
                print("Invalid choice. Please select a valid option.")

if __name__ == "__main__":
    app = BudgetTrackerApp()
    app.run()
