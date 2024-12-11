
from datetime import datetime

class BudgetCalculator:
    def __init__(self, db_manager):
        self.db_manager = db_manager

    def calculate_income(self):
        month_year = datetime.now().strftime("%B-%Y")
        incomes = self.db_manager.get_income()
        return sum(income[2] for income in incomes if income[3] == month_year)

    def calculate_total_expenses(self):
        month_year = datetime.now().strftime("%B-%Y")
        budget_status = self.db_manager.get_budget_status_for_month(month_year)
        return sum(row[2] for row in budget_status)

    def calculate_remaining_budget(self):
        month_year = datetime.now().strftime("%B-%Y")
        budget_status = self.db_manager.get_budget_status_for_month(month_year)
        total_allocated = sum(row[1] for row in budget_status)
        total_spent = sum(row[2] for row in budget_status)
        return total_allocated - total_spent

    def calculate_savings(self):
        all_incomes = self.db_manager.get_income()
        total_income = sum(income[2] for income in all_incomes)
        all_budgets = self.db_manager.get_budget_status_for_month(datetime.now().strftime("%B-%Y"))
        total_expenses = sum(row[2] for row in all_budgets)
        return total_income - total_expenses
