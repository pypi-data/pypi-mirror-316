from SmartBudget import TransactionManager, Analysis

def test_analysis():
    print("Тест: Analysis")

    manager = TransactionManager()
    manager.add_transaction(500, "Зарплата", "+")
    manager.add_transaction(200, "Еда", "-")
    manager.add_transaction(50, "Транспорт", "-")
    manager.add_transaction(50, "Транспорт", "-")

    summary = Analysis.category_summary(manager.transactions)
    assert summary == {"Зарплата": 500, "Еда": -200, "Транспорт": -100}, "Ошибка в сводке по категориям"

    percentage = Analysis.percentage_spent(manager.transactions)
    assert percentage == {"Еда": 66.66666666666666, "Транспорт": 33.33333333333333}, "Ошибка в расчете процентов расходов"

    print("Analysis успешно прошел тесты!")

if __name__ == "__main__":
    test_analysis()
