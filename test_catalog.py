"""Проверка вывода полей."""
import database as db


def test_fields():
    """Проверяет, что все поля на месте."""
    products = db.get_all_products()
    print(f"Всего товаров: {len(products)}")

    required_count = 6
    errors = 0

    for p in products:
        if len(p) < required_count:
            print(f"❌ Товар id={p[0]}: мало полей ({len(p)})")
            errors += 1

    if errors == 0:
        print("✅ Все товары содержат нужные поля")
    else:
        print(f"❌ Найдено ошибок: {errors}")


def test_prices():
    """Проверяет, что у всех товаров есть цена."""
    products = db.get_all_products()
    for p in products:
        if p[4] is None:
            print(f"❌ Товар id={p[0]}: нет цены")
            return
    print("✅ У всех товаров есть цена")


def test_quantities():
    """Проверяет, что у всех товаров количество ≥ 0."""
    products = db.get_all_products()
    for p in products:
        if p[5] is None or p[5] < 0:
            print(f"❌ Товар id={p[0]}: некорректное количество")
            return
    print("✅ У всех товаров количество ≥ 0")


def test_images():
    """Проверяет, что хотя бы у одного товара есть изображение."""
    products = db.get_all_products()
    has_image = any(p[6] for p in products)
    if has_image:
        print("✅ Хотя бы у одного товара есть изображение")
    else:
        print("⚠️ Ни у одного товара нет изображения (все с заглушкой)")


if __name__ == "__main__":
    test_fields()
    test_prices()
    test_quantities()
    test_images()