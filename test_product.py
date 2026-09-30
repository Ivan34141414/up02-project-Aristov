"""Проверка класса Product."""
from models import Product


# Создаём один товар вручную
p = Product(
    product_id=1,
    name="Смирнова О.А.",
    category="Терапевт",
    exp=12,
    price=2200,
    quantity=8,
    image="doctor1.png",
)

print(p.info())
print(f"Со скидкой 25%: {p.price_with_discount(25):.2f} руб.")
