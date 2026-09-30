"""Тестирование алгоритма скидки."""
from datetime import datetime
from discount import calculate_price_with_discount


def run_tests():
    """Прогон тестов."""
    date = datetime(2026, 10, 15)

    test_cases = [
        (1, 2200, 2200, "Смирнова — есть заказ 15.09"),
        (2, 3200, 3200, "Иванов — есть заказ 20.09"),
        (3, 3000, 3000, "Петрова — есть заказ 25.09"),
        (4, 2700, 2025, "Сидоров — скидка"),
        (5, 2600, 1950, "Кузнецов — скидка"),
        (6, 3800, 2850, "Морозов — скидка"),
        (7, 2000, 1500, "Волкова — скидка"),
    ]

    print("=" * 60)
    print("ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ")
    print("=" * 60)

    passed = 0
    for product_id, price, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Врач {product_id}: {price} → {result} "
              f"(ожидалось {expected}) — {comment}")

    print("=" * 60)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    run_tests()
    