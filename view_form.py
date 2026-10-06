"""Форма просмотра товара."""
import tkinter as tk
from tkinter import ttk, messagebox

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, FONT_SIZE_TITLE, font
)
from resources import load_image, get_product_image
from order_manager import (
    add_order_to_db,
    update_product_quantity,
    get_product_quantity
)


class ViewForm:
    """Форма просмотра выбранного товара."""

    def __init__(self, parent, product, on_add_to_order=None):
        self.product = product
        self.on_add_to_order = on_add_to_order

        self.window = tk.Toplevel(parent)
        self.window.title(f"Просмотр — {product[2]}")
        self.window.geometry("700x600")
        self.window.configure(bg=COLOR_MAIN_BG)

        self.build_ui()
        

    def build_ui(self):
        """Строит интерфейс формы."""
        # Шапка
        header = tk.Frame(self.window, bg=COLOR_SECONDARY_BG, height=60)
        header.pack(fill="x")
        header.pack_propagate(False)
        tk.Label(header, text="КАРТОЧКА ВРАЧА",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(pady=15)

        # Основная область
        main = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        main.pack(fill="both", expand=True, padx=20, pady=20)

        # Изображение (слева)
        img_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        img_frame.pack(side="left", padx=10)
        photo = get_product_image(self.product[6], size=(200, 200))
        if photo:
            img_label = tk.Label(img_frame, image=photo, bg=COLOR_MAIN_BG)
            img_label.image = photo
            img_label.pack()

        # Информация (справа)
        info_frame = tk.Frame(main, bg=COLOR_MAIN_BG)
        info_frame.pack(side="left", fill="both", expand=True, padx=20)

        # Поля формы
        self._add_field(info_frame, "ФИО", self.product[2])
        self._add_field(info_frame, "Специальность", self.product[1])
        self._add_field(info_frame, "Стаж", f"{self.product[3]} лет")
        self._add_field(info_frame, "Цена", f"{self.product[4]:.0f} руб.")
        self._add_field(info_frame, "Количество", self.product[5])

        # Поле ввода количества
        qty_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        qty_frame.pack(fill="x", pady=5, padx=20)

        tk.Label(qty_frame, text="Введите количество:",
                 font=font(FONT_SIZE_NORMAL, bold=True),
                 bg=COLOR_MAIN_BG).pack(side="left", padx=10)

        self.qty_entry = tk.Entry(qty_frame)
        self.qty_entry.pack(side="left")

        tk.Button(qty_frame, text="Проверить",
                  command=self._check_qty,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL)).pack(side="left", padx=10)

        # Кнопки
        btn_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        btn_frame.pack(fill="x", pady=10)

        tk.Button(btn_frame, text="Добавить в заказ",
                  command=self.add_to_order,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="left", padx=20)

        tk.Button(btn_frame, text="Назад",
                  command=self.window.destroy,
                  bg=COLOR_ACCENT, fg="white",
                  font=font(FONT_SIZE_NORMAL),
                  padx=15, pady=5).pack(side="right", padx=20)

    def _add_field(self, parent, label, value):
        """Добавляет поле в форму."""
        row = tk.Frame(parent, bg=COLOR_MAIN_BG)
        row.pack(fill="x", pady=3)

        tk.Label(row, text=f"{label}:",
                 font=font(FONT_SIZE_NORMAL, bold=True),
                 width=15, anchor="w",
                 bg=COLOR_MAIN_BG).pack(side="left")

        tk.Label(row, text=str(value),
                 font=font(FONT_SIZE_NORMAL),
                 anchor="w",
                 bg=COLOR_MAIN_BG).pack(side="left")
        

    def add_to_order(self):
        """Обработчик кнопки «Добавить в заказ»."""
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return

        try:
            product_id = self.product[0]
            current_qty = get_product_quantity(product_id)

            if current_qty < 1:
                messagebox.showwarning("Товар закончился",
                                       f"Врача «{self.product[2]}» больше нет")
                return

            new_qty = current_qty - 1

            add_order_to_db("Иванов Иван Иванович", product_id, 1)
            update_product_quantity(product_id, new_qty)

            messagebox.showinfo("Успех", "Заказ оформлен")

            if self.on_add_to_order:
                self.on_add_to_order()

        except Exception as e:
            messagebox.showerror("Ошибка заказа",
                                 f"Не удалось оформить заказ:\n{e}")
            

    def _check_qty(self):
        """Проверяет введённое количество (ДЗ)."""
        from error_handler import validate_positive_int
        ok, result = validate_positive_int(self.qty_entry.get(), "Количество")
        if ok:
            messagebox.showinfo("OK", f"Введено число: {result}")
        else:
            messagebox.showwarning("Ошибка", result)