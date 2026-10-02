"""Каталог товаров."""
import tkinter as tk

from styles import (
    COLOR_HIGHLIGHT, COLOR_MAIN_BG,
    FONT_SIZE_NORMAL, FONT_SIZE_HEADER, font
)
from resources import get_product_image


def create_product_card(parent, product):
    qty = product[5]
    bg_color = COLOR_HIGHLIGHT if qty <= 3 else COLOR_MAIN_BG

    card = tk.Frame(parent, bg=bg_color, bd=1, relief="solid")
    card.pack(fill="x", padx=10, pady=5)

    img_frame = tk.Frame(card, bg=bg_color)
    img_frame.pack(side="left", padx=10, pady=10)

    photo = get_product_image(product[6], size=(100, 100))
    if photo:
        img_label = tk.Label(img_frame, image=photo, bg=bg_color)
        img_label.image = photo
        img_label.pack()
    else:
        tk.Label(img_frame, text="[НЕТ ФОТО]", bg=bg_color,
                 width=10, height=5).pack()

    text_frame = tk.Frame(card, bg=bg_color)
    text_frame.pack(side="left", fill="both", expand=True, padx=10, pady=10)

    title = f"{product[2]} | {product[1]}"
    tk.Label(text_frame, text=title, font=font(FONT_SIZE_HEADER, bold=True),
             bg=bg_color, anchor="w").pack(fill="x")

    indicator = "много" if qty > 5 else "мало"
    tk.Label(text_frame, text=f"Количество: {indicator} ({qty})",
             font=font(FONT_SIZE_NORMAL), bg=bg_color, anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"Стаж: {product[3]} лет",
             font=font(FONT_SIZE_NORMAL), bg=bg_color, anchor="w").pack(fill="x")

    tk.Label(text_frame, text=f"{product[4]:.0f} руб.",
             font=font(FONT_SIZE_HEADER, bold=True),
             bg=bg_color, anchor="e").pack(fill="x")

    tk.Frame(parent, bg="#cccccc", height=1).pack(fill="x", padx=10)

    return card