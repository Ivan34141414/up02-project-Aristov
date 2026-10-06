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
    add_order_item,
    update_product_quantity,
    get_product_quantity
)
from db_products import get_product_sizes
from error_handler import validate_positive_int


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

        # == Поле ввода количества ==
        qty_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        qty_frame.pack(fill="x", pady=10, padx=20)

        tk.Label(qty_frame, text="Количество:",
                 font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG).pack(side="left", padx=5)
    
        self.qty_var = tk.StringVar(value="1")
        qty_entry = tk.Entry(qty_frame, textvariable=self.qty_var,
                             width=5, font=font(FONT_SIZE_NORMAL))
        qty_entry.pack(side="left", padx=5)

        # == Выбор размера ==
        size_frame = tk.Frame(self.window, bg=COLOR_MAIN_BG)
        size_frame.pack(fill="x", pady=10, padx=20)

        tk.Label(size_frame, text="Размер:",
                 font=font(FONT_SIZE_NORMAL),
                 bg=COLOR_MAIN_BG).pack(side="left", padx=5)

        sizes = get_product_sizes(self.product[0])
        if not sizes:
            sizes = ["—"]

        self.size_var = tk.StringVar(value=sizes[0])
        size_combo = ttk.Combobox(size_frame, textvariable=self.size_var,
                                  values=sizes, state="readonly",
                                  width=5, font=font(FONT_SIZE_NORMAL))
        size_combo.pack(side="left", padx=5)

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
        # 1. Проверяем товар
        if not self.product:
            messagebox.showerror("Ошибка", "Товар не выбран")
            return

        # 2. Валидация количества
        ok, result = validate_positive_int(self.qty_var.get(), "Количество")
        if not ok:
            messagebox.showwarning("Ошибка ввода", result)
            return
        qty = result

        # 3. Проверяем, что количество не больше доступного
        current_qty = get_product_quantity(self.product[0])
        if qty > current_qty:
            messagebox.showwarning("Ошибка",
                                   f"Доступно только {current_qty} шт.")
            return

        # 4. Оформляем заказ
        try:
            # Создаём заказ (только клиент)
            order_id = add_order_to_db("Иванов Иван Иванович")

            # Добавляем позицию в состав (размер 0 — у нас нет размеров)
            price = float(self.product[4])
            add_order_item(order_id, self.product[0], qty, price)

            # Обновляем количество товара
            new_qty = current_qty - qty
            update_product_quantity(self.product[0], new_qty)

            messagebox.showinfo("Успех",
                                f"Товар добавлен в заказ ({qty}) шт.")

            if self.on_add_to_order:
                self.on_add_to_order(self.product, qty, self.size_var.get())

            self.window.destroy()

        except Exception as e:
            messagebox.showerror("Ошибка заказа",
                                 f"Не удалось оформить заказ:\n{e}")