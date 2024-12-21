from SmartBudget import TransactionManager

def test_transaction_manager():
    print("Тест: TransactionManager")

    manager = TransactionManager()
    manager.add_transaction(500, "Зарплата", "+")
    manager.add_transaction(150, "Еда", "-")
    manager.add_transaction(50, "Еда", "-")
    manager.add_transaction(50, "Транспорт", "-")

    # Проверка баланса
    assert manager.get_balance() == 250, "Ошибка в расчете баланса"

    # Проверка категории
    food_transactions = manager.filter_by_category("Еда")
    assert food_transactions == ("- 150 (Еда)\n- 50 (Еда)"), "Ошибка в фильтрации транзакций"
    assert manager.filter_by_category("Транспорт") == "- 50 (Транспорт)", "Ошибка в фильтрации транзакций"

    # Проверка пустой категории
    assert manager.filter_by_category("Одежда") == "Транзакции по категории 'Одежда' не найдены.", "Ошибка, ожидается сообщение о пустой категории"

    manager.add_transaction(200, "Еда", "-")
    manager.remove_transaction(5)
    assert len(manager.transactions) == 4, "Ошибка в удалении транзакции"

    manager.clear_transactions()
    assert len(manager.transactions) == 0, "Ошибка в очистке всех транзакций"

    manager.add_transaction(500, "Зарплата", "+")
    manager.add_transaction(200, "Еда", "-")
    assert manager.total_income() == 500, "Ошибка в подсчете доходов"
    assert manager.total_expenses() == 200, "Ошибка в подсчете расходов"

    print("TransactionManager успешно прошел тесты!")

if __name__ == "__main__":
    test_transaction_manager()
