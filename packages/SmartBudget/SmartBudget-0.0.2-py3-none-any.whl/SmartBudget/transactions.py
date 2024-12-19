class Transaction:
    def __init__(self, amount, category, transaction_type):
        self.amount = amount
        self.category = category
        self.type = transaction_type

    def __str__(self):
        return f"{self.type.title()} {self.amount} ({self.category})"

class TransactionManager:
    def __init__(self):
        self.transactions = []

    # Добавление транзакции
    def add_transaction(self, amount, category, transaction_type):
        if transaction_type not in ["+", "-"]:
            raise ValueError("Тип транзакции должен быть '+' или '-'")
        transaction = Transaction(amount, category, transaction_type)
        self.transactions.append(transaction)
        return transaction  # Возвращаем объект транзакции

    # Вычисляет текущий баланс
    def get_balance(self):
        income = sum(t.amount for t in self.transactions if t.type == "+")
        expenses = sum(t.amount for t in self.transactions if t.type == "-")
        return income - expenses

    # Удаление транзакции
    def remove_transaction(self, index):
        index = index - 1
        if index < 0 or index >= len(self.transactions):
            raise IndexError("Нет такой транзакции!!")
        self.transactions.pop(index)

    # Удаляет все транзакции
    def clear_transactions(self):
        self.transactions.clear()

    # Всего доходов
    def total_income(self):
        return sum(t.amount for t in self.transactions if t.type == "+")

    # Всего расходов
    def total_expenses(self):
        return sum(t.amount for t in self.transactions if t.type == "-")

    # Возвращает строковое представление транзакций по указанной категории
    def filter_by_category(self, category):
        filtered_transactions = [transaction for transaction in self.transactions if transaction.category == category]

        # Преобразуем список транзакций в строку
        if filtered_transactions:
            return "\n".join(str(transaction) for transaction in filtered_transactions)
        else:
            return f"Транзакции по категории '{category}' не найдены."


