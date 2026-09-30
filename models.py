"""Модели данных для проекта УП.02."""


class Product:
    """Класс Товар."""

    def __init__(self, product_id, name, category, exp, price, quantity, image):
        """
        Инициализация товара.

        :param product_id: идентификатор
        :param name: ФИО
        :param category: специальность
        :param exp: стаж
        :param price: цена
        :param quantity: количество
        :param image: фото
        """
        self.id = product_id
        self.name = name
        self.category = category
        self.exp = exp
        self.price = price
        self.quantity = quantity
        self.image = image

    def total(self):
        """Общая стоимость (цена × количество)."""
        return self.price * self.quantity

    def price_with_discount(self, discount_percent):
        """Цена со скидкой."""
        return self.price * (1 - discount_percent / 100)

    def indicator(self):
        """Индикатор «много/мало» (порог 5)."""
        return "много" if self.quantity > 5 else "мало"

    def info(self):
        """Строка с информацией о товаре."""
        return (
            f"{self.name} ({self.category}): "
            f"{self.price} руб. × {self.quantity} = {self.total()} руб. "
            f"({self.indicator()})"
        )
