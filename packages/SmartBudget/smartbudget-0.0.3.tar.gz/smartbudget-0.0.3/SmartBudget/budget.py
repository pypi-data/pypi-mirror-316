class Budget:
    def __init__(self, total_budget):
        self.total_budget = total_budget
        self.category_limits = {}

    # Устанавливает лимит для категории
    def set_category_limit(self, category, limit):
        self.category_limits[category] = limit

    # Удаляет лимит для категории
    def remove_category_limit(self, category):
        if category in self.category_limits:
            del self.category_limits[category]
        else:
            print(f"Лимит для категории '{category}' не найден.")

    # Удаляет все лимиты
    def clear_limits(self):
        self.category_limits.clear()

    # Проверяет, превышен ли бюджет по категории
    def is_category_exceeded(self, transactions, category):
        if category not in self.category_limits:
            print(f"Лимит для категории '{category}' не установлен.")
            return False
        total_spent = sum(t.amount for t in transactions if t.category == category and t.type == "-")
        return total_spent > self.category_limits[category]

    # Возвращает список категорий, где расходы превысили лимиты
    def exceeded_categories(self, transactions):
        exceeded = {}
        for category, limit in self.category_limits.items():
            total_spent = sum(t.amount for t in transactions if t.category == category and t.type == "-")
            if total_spent > limit:
                exceeded[category] = total_spent
        return exceeded

    # Возвращает текущие лимиты для всех категорий
    def get_category_limits(self):
        return self.category_limits
