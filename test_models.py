from datetime import datetime
from models import Product

p = Product(6, "Морозов Д.Д.", "Стоматолог", 10, 3800, 3, "doctor6.png")
date = datetime(2026, 10, 15)
print(f"Базовая цена: {p.price}")
print(f"Со скидкой: {p.price_with_discount_auto(date)}")
