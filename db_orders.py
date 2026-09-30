"""Загрузка заказов из БД в объекты класса Order."""
import sqlite3
from config import DB_PATH
from models import Product, Order


def get_all_products():
    """Все товары из БД в виде словаря {id: объект Product}."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()

    products = {}
    for row in rows:
        p = Product(row[0], row[2], row[1], row[3], row[4], row[5], row[6])
        products[p.id] = p
    return products


def get_all_orders():
    """Все заказы из БД в виде списка объектов Order."""
    products = get_all_products()

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Заказ ORDER BY id")
    rows = cur.fetchall()
    conn.close()

    orders = []
    for row in rows:
        product = products.get(row[3])
        if product is None:
            continue
        order = Order(row[0], row[1], row[2], product, row[4])
        orders.append(order)
    return orders


def print_orders(orders):
    """Вывод заказов."""
    print(f"\nВсего заказов: {len(orders)}\n")
    for o in orders:
        print(o.info())
        print("-" * 60)


if __name__ == "__main__":
    orders = get_all_orders()
    print_orders(orders)