class Product:
    def __init__(self, name, price, image_url):
        self.name = name
        self.price = price
        self.image_url = image_url

    def to_dict(self):
        """Convertit l'objet Product en dictionnaire pour MongoDB."""
        return {
            "name": self.name,
            "price": self.price,
            "image_url": self.image_url,
        }
