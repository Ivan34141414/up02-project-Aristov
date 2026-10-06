"""Обработка исключений."""
from tkinter import messagebox


def safe_call(func, *args, **kwargs):
    """Безопасный вызов функции."""
    try:
        return func(*args, **kwargs)
    except FileNotFoundError as e:
        messagebox.showerror("Ошибка файла", f"Файл не найден:\n{e}")
    except ConnectionError as e:
        messagebox.showerror("Ошибка соединения", f"Нет соединения:\n{e}")
    except ValueError as e:
        messagebox.showwarning("Ошибка значения", f"Некорректное значение:\n{e}")
    except Exception as e:
        messagebox.showerror("Ошибка", f"Произошла ошибка:\n{e}")
    return None


def validate_positive_int(value, field_name="Значение"):
    """
    Проверяет, что значение — положительное целое число.
    :param value: строка для проверки
    :param field_name: название поля (для сообщения)
    :return: (True, число) или (False, сообщение)
    """
    try:
        number = int(value)
    except ValueError:
        return (False, f"{field_name} должно быть целым числом")

    if number <= 0:
        return (False, f"{field_name} должно быть больше нуля")

    return (True, number)
