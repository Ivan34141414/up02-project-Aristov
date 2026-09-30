"""Загрузка товаров из БД в объекты класса Product."""
import sqlite3
from config import DB_PATH
from models import Product


def get_all_products():
    """Возвращает список объектов Product из БД."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()	

    products = []
    for row in rows:
        product = Product(
            product_id=row[0],
            name=row[2],
            category=row[1],
            exp=row[3],
            price=row[4],
            quantity=row[5],
            image=row[6],
        )
        products.append(product)
    return products

def get_products_by_category(category):
    """Возвращает список объектов Product по категории."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE специальность = ?", (category,))
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = Product(
            product_id=row[0],
            name=row[2],
            category=row[1],
            exp=row[3],
            price=row[4],
            quantity=row[5],
            image=row[6],
        )
        products.append(product)
    return products

def get_products_low_stock():
    """Возвращает товары с количеством ≤ 3."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар WHERE количество <= 3")
    rows = cur.fetchall()
    conn.close()

    products = []
    for row in rows:
        product = Product(
            product_id=row[0],
            name=row[2],
            category=row[1],
            exp=row[3],
            price=row[4],
            quantity=row[5],
            image=row[6],
        )
        products.append(product)
    return products

def print_catalog_with_highlight(products):
    """Выводит каталог с подсветкой для товаров ≤3."""
    print(f"\n{'=' * 70}")
    print(f"КАТАЛОГ ({len(products)} товаров)")
    print("=" * 70)

    for p in products:
        highlight = "⚠️" if p.quantity <= 3 else "  "
        print(f"{highlight} {p.info()}")

    print("=" * 70)


def print_products(products):
    """Выводит информацию о товарах."""
    print(f"\nВсего товаров: {len(products)}\n")
    for p in products:
        print(p.info())
        print("-" * 60)


if __name__ == "__main__":
    print("1. Все товары:")
    print_catalog_with_highlight(get_all_products())

    print("\n2. Товары категории «Хирург»:")
    print_catalog_with_highlight(get_products_by_category("Хирург"))

    print("\n3. Товары с низким остатком (≤3):")
    print_catalog_with_highlight(get_products_low_stock())

