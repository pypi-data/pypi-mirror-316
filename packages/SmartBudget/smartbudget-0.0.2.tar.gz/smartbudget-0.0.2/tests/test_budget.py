from SmartBudget import TransactionManager, Budget

def test_budget_limits():
    print("Тест: Лимиты бюджета")

    # Создаем экземпляр Budget
    budget = Budget(1000)

    # Устанавливаем лимиты для категорий
    budget.set_category_limit("Еда", 300)
    budget.set_category_limit("Транспорт", 150)

    # Проверяем лимиты
    assert budget.get_category_limits() == {"Еда": 300, "Транспорт": 150}, "Ошибка: Неверно установлены лимиты"

    # Проверяем удаление лимита
    budget.remove_category_limit("Транспорт")
    assert budget.get_category_limits() == {"Еда": 300}, "Ошибка: Лимит для 'Транспорт' не удален"

    # Проверяем удаление несуществующего лимита
    budget.remove_category_limit("Одежда")

    # Удаляем все лимиты
    budget.clear_limits()
    assert budget.get_category_limits() == {}, "Ошибка: Лимиты не очищены"

    print("Лимиты бюджета успешно прошли тесты!\n")

def test_budget_category_exceeded():
    print("Тест: Проверка превышения по категориям")

    # Создаем экземпляр Budget и устанавливаем лимиты
    budget = Budget(1000)
    budget.set_category_limit("Еда", 300)
    budget.set_category_limit("Транспорт", 150)

    # Создаем транзакции
    manager = TransactionManager()
    transactions = [
        manager.add_transaction(100, "Еда", "-"),
        manager.add_transaction(250, "Еда", "-"),
        manager.add_transaction(100, "Транспорт", "-"),
        manager.add_transaction(100, "Развлечения", "-")
    ]

    # Проверяем превышение по категориям
    assert budget.is_category_exceeded(transactions, "Еда"), "Ошибка: Лимит для 'Еда' должен быть превышен"
    assert not budget.is_category_exceeded(transactions, "Транспорт"), "Ошибка: Лимит для 'Транспорт' не должен быть превышен"

    # Проверяем несуществующий лимит
    assert not budget.is_category_exceeded(transactions, "Развлечения"), "Ошибка: Лимит для 'Развлечения' не установлен, но вернул превышение"

    # Проверяем список категорий с превышением
    exceeded = budget.exceeded_categories(transactions)
    assert exceeded == {"Еда": 350}, "Ошибка: Неверно определены категории с превышением"

    print("Проверка превышения по категориям успешно прошла тесты!\n")

def test_budget_operations():
    print("Тест: Операции с лимитами")

    # Создаем экземпляр Budget и добавляем лимиты
    budget = Budget(1000)
    budget.set_category_limit("Еда", 300)
    budget.set_category_limit("Транспорт", 150)

    # Удаляем лимит, добавляем обратно
    budget.remove_category_limit("Еда")
    budget.set_category_limit("Еда", 400)

    # Проверяем текущие лимиты
    assert budget.get_category_limits() == {"Еда": 400, "Транспорт": 150}, "Ошибка: Неверно обработаны изменения лимитов"

    # Проверяем очистку и добавление новых лимитов
    budget.clear_limits()
    assert budget.get_category_limits() == {}, "Ошибка: Лимиты не очищены"
    budget.set_category_limit("Развлечения", 200)
    assert budget.get_category_limits() == {"Развлечения": 200}, "Ошибка: Лимит для 'Развлечения' не установлен после очистки"

    print("Операции успешно прошли тесты!\n")

if __name__ == "__main__":
    test_budget_limits()
    test_budget_category_exceeded()
    test_budget_operations()
    print("Все тесты для Budget успешно пройдены!")
