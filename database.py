"""Работа с базой данных."""
import sqlite3
from config import DB_PATH


def get_all_products():
    """Возвращает список всех товаров из БД."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT * FROM Товар ORDER BY id")
    rows = cur.fetchall()
    conn.close()
    return rows


def get_categories():
    """Список всех специальностей."""
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()
    cur.execute("SELECT DISTINCT специальность FROM Товар ORDER BY специальность")
    categories = [row[0] for row in cur.fetchall()]
    conn.close()
    return categories