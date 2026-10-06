"""Работа с заказами."""
import sqlite3
from datetime import datetime
from config import DB_PATH


def get_connection():
    """Соединение с БД."""
    return sqlite3.connect(DB_PATH)


def add_order_to_db(client, product_id, quantity):
    """
    Добавляет новый заказ в БД.
    :param client: ФИО клиента
    :param product_id: id товара
    :param quantity: количество
    :return: id заказа или None при ошибке
    """
    conn = get_connection()
    cur = conn.cursor()

    дата = datetime.now().strftime("%Y-%m-%d")

    cur.execute(
        "INSERT INTO Заказ (дата, клиент, товар_id, количество) "
        "VALUES (?, ?, ?, ?)",
        (дата, client, product_id, quantity)
    )
    conn.commit()

    order_id = cur.lastrowid
    conn.close()

    return order_id


def update_product_quantity(product_id, new_quantity):
    """
    Обновляет количество товара в БД.
    :param product_id: id товара
    :param new_quantity: новое количество
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute(
        "UPDATE Товар SET количество = ? WHERE id = ?",
        (new_quantity, product_id)
    )
    conn.commit()
    conn.close()


def get_last_order_id():
    """
    Возвращает id последнего заказа.
    :return: id или None
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT MAX(id) FROM Заказ")
    row = cur.fetchone()
    conn.close()

    return row[0] if row else None


def get_product_quantity(product_id):
    """
    Возвращает количество товара по id.
    :param product_id: id товара
    :return: количество или 0
    """
    conn = get_connection()
    cur = conn.cursor()

    cur.execute("SELECT количество FROM Товар WHERE id = ?", (product_id,))
    row = cur.fetchone()
    conn.close()

    return row[0] if row else 0