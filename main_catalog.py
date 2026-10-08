"""Главное окно приложения."""
import tkinter as tk
from tkinter import ttk

from styles import (
    COLOR_MAIN_BG, COLOR_SECONDARY_BG, COLOR_ACCENT,
    FONT_SIZE_NORMAL, FONT_SIZE_TITLE, font
)
from config import APP_TITLE
import database as db
from catalog import create_product_card
from resources import load_image_proportional, PATH_LOGO, PATH_ICON
from error_handler import safe_call


def set_app_icon(root, icon_path):
    """Устанавливает иконку приложения."""
    import os
    try:
        if os.name == "nt":
            if os.path.exists(icon_path):
                root.iconbitmap(icon_path)
        else:
            png_path = icon_path.replace(".ico", ".png")
            icon_img = load_image_proportional(png_path, max_size=(32, 32))
            if icon_img:
                root.iconphoto(True, icon_img)
                root._icon_photo = icon_img
    except Exception as e:
        print(f"Не удалось установить иконку: {e}")


class MainWindow:
    """Главное окно приложения."""

    def __init__(self):
        self.root = tk.Tk()
        self.root.title(APP_TITLE)
        self.root.geometry("900x700")
        self.root.configure(bg=COLOR_MAIN_BG)

        self.current_user = None
        self.user_label = None

        set_app_icon(self.root, PATH_ICON)

        self.build_ui()
        self.load_products()
        self.require_auth()

    def build_ui(self):
        """Строит интерфейс окна."""
        header = tk.Frame(self.root, bg=COLOR_SECONDARY_BG, height=80)
        header.pack(fill="x")
        header.pack_propagate(False)

        logo = load_image_proportional(PATH_LOGO, max_size=(60, 60))
        if logo:
            logo_label = tk.Label(header, image=logo, bg=COLOR_SECONDARY_BG)
            logo_label.image = logo
            logo_label.pack(side="left", padx=15)

        tk.Label(header, text="КАТАЛОГ ВРАЧЕЙ",
                 font=font(FONT_SIZE_TITLE, bold=True),
                 bg=COLOR_SECONDARY_BG).pack(side="left", expand=True)

        # ФИО пользователя
        self.user_label = tk.Label(header, text="Не авторизован",
                                   font=font(FONT_SIZE_NORMAL),
                                   bg=COLOR_SECONDARY_BG)
        self.user_label.pack(side="right", padx=15)

        # Область с прокруткой
        self.canvas = tk.Canvas(self.root, bg="white", highlightthickness=0)
        scrollbar = ttk.Scrollbar(self.root, orient="vertical",
                                  command=self.canvas.yview)
        self.catalog_frame = tk.Frame(self.canvas, bg="white")
        self.catalog_frame.bind(
            "<Configure>",
            lambda e: self.canvas.configure(
                scrollregion=self.canvas.bbox("all"))
        )
        self.canvas.create_window((0, 0), window=self.catalog_frame,
                                  anchor="nw")
        self.canvas.configure(yscrollcommand=scrollbar.set)

        self.canvas.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def require_auth(self):
        """Запрашивает авторизацию."""
        from auth import AuthWindow
        AuthWindow(self.root, self.on_auth_success)

    def on_auth_success(self, user):
        """Обработчик успешной авторизации."""
        self.current_user = user

        fio = f"{user[1]} {user[2]} {user[3] or ''}".strip()
        self.user_label.config(text=f"{fio} ({user[5]})")

        self.add_role_buttons(user[5])

    def add_role_buttons(self, role):
        """Добавляет кнопки в зависимости от роли."""
        header = self.user_label.master

        if role in ("Менеджер", "Администратор"):
            tk.Button(header, text="Заказы",
                      command=self.open_orders,
                      bg=COLOR_ACCENT, fg="white",
                      font=font(FONT_SIZE_NORMAL),
                      padx=10, pady=5).pack(side="right", padx=10)

        if role == "Администратор":
            tk.Button(header, text="Админ-панель",
                      command=self.open_admin,
                      bg=COLOR_ACCENT, fg="white",
                      font=font(FONT_SIZE_NORMAL),
                      padx=10, pady=5).pack(side="right", padx=10)

    def open_orders(self):
        """Открывает окно списка заказов."""
        from orders_window import OrdersWindow
        OrdersWindow(self.root, self.current_user)

    def open_admin(self):
        """Заглушка для админ-панели."""
        from tkinter import messagebox
        messagebox.showinfo("Админ-панель", "В разработке")

    def load_products(self):
        """Загружает товары в каталог."""
        products = safe_call(db.get_all_products) or []
        for p in products:
            safe_call(create_product_card, self.catalog_frame, p,
                      refresh=self.refresh_catalog)

    def refresh_catalog(self, *args):
        """Обновляет каталог. *args — для совместимости."""
        for widget in self.catalog_frame.winfo_children():
            widget.destroy()
        self.load_products()

    def run(self):
        """Запускает приложение."""
        self.root.mainloop()


if __name__ == "__main__":
    MainWindow().run()