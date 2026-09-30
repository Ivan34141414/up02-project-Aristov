"""Тестирование алгоритма скидки."""
from datetime import datetime
from discount import calculate_price_with_discount


def run_tests():
    test_cases = [
        # (product_id, price, date, expected, comment)
        (1, 2200, datetime(2026, 10, 15), 2200, "Заказы есть в сентябре"),
        (2, 3200, datetime(2026, 10, 15), 3200, "Заказы есть в сентябре"),
        (3, 3000, datetime(2026, 10, 15), 3000, "Заказы есть в сентябре"),
        (4, 2700, datetime(2026, 10, 15), 2025, "Заказов нет - скидка"),
        (5, 2600, datetime(2026, 10, 15), 1950, "Заказов нет - скидка"),
        (6, 3800, datetime(2026, 10, 15), 2850, "Заказов нет - скидка"),
        (7, 2000, datetime(2026, 10, 15), 1500, "Заказов нет - скидка"),
        # Новые тесты
        (4, 2700, datetime(2026, 11, 15), 2025, "В октябре заказов не было"),
        (6, 3800, datetime(2026, 11, 15), 2850, "В октябре заказов не было"),
        (4, 2700, datetime(2026, 9, 1), 2025, "В августе заказов не было"),
        (1, 2200, datetime(2026, 11, 15), 1650, "Октябрь: заказов нет — скидка"),
        (7, 2000, datetime(2026, 12, 15), 1500, "Ноябрь: заказов нет — скидка"),
    ]


    print("=" * 70)
    print("РАСШИРЕННОЕ ТЕСТИРОВАНИЕ АЛГОРИТМА СКИДКИ")
    print("=" * 70)

    passed = 0
    for product_id, price, date, expected, comment in test_cases:
        result = calculate_price_with_discount(product_id, price, date)
        status = "✅" if result == expected else "❌"
        if result == expected:
            passed += 1
        print(f"{status} Врач {product_id} на {date.date()}: "
              f"{price} → {result} (ожидалось {expected}) — {comment}")

    print("=" * 70)
    print(f"Пройдено: {passed} / {len(test_cases)}")


if __name__ == "__main__":
    run_tests()