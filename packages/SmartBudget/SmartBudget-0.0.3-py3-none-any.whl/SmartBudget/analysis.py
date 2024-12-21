class Analysis:
    @staticmethod
    # Считает расходы/доходы по категориям
    def category_summary(transactions):
        summary = {}
        for transaction in transactions:
            if transaction.category not in summary:
                summary[transaction.category] = 0
            if transaction.type == "+":
                summary[transaction.category] += transaction.amount
            else:
                summary[transaction.category] -= transaction.amount
        return summary

    @staticmethod
    # Возвращает процент расходов по категориям
    def percentage_spent(transactions):
        total_expenses = sum(t.amount for t in transactions if t.type == "-")
        if total_expenses == 0:
            return {}

        percentage = {}
        for transaction in transactions:
            if transaction.type == "-":
                if transaction.category not in percentage:
                    percentage[transaction.category] = 0
                percentage[transaction.category] += transaction.amount

        # Переводим сумму расходов в процент от общей суммы расходов
        for category in percentage:
            percentage[category] = (percentage[category] / total_expenses) * 100

        return percentage
