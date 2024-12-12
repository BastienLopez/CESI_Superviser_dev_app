import mongoengine as db


class Products(db.Document):
    id = db.SequenceField(primary_key=True)
    name = db.StringField(required=True, max_length=100)
    description = db.StringField()
    price = db.FloatField(required=True)
    image = db.StringField()
    storage_quantity = db.IntField(required=True)

    def __repr__(self):
        return f'<Product {self.name}>'