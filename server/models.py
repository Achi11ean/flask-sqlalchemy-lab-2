from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import MetaData
from sqlalchemy.ext.associationproxy import association_proxy
from sqlalchemy_serializer import SerializerMixin


metadata = MetaData(naming_convention={
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
})

db = SQLAlchemy(metadata=metadata)

# Review Model
class Review(db.Model, SerializerMixin):
    __tablename__ = 'reviews'
    id = db.Column(db.Integer, primary_key=True)
    comment = db.Column(db.String, nullable=False)
    customer_id = db.Column(db.Integer, db.ForeignKey('customers.id'), nullable=True)
    item_id = db.Column(db.Integer, db.ForeignKey('items.id'), nullable=True)

    customer = db.relationship('Customer', backref='reviews')
    item = db.relationship('Item', backref='reviews')

    serialize_rules = ('-customer.reviews', '-item.reviews')

    def __init__(self, comment='', customer=None, item=None):
        self.comment = comment
        self.customer = customer
        self.item = item

# Customer Model with Association Proxy
class Customer(db.Model, SerializerMixin):
    __tablename__ = 'customers'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    items = association_proxy('reviews', 'item')
    serialize_rules = ('-reviews',)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            # Handle cases where item might be None
            'items': [item.name for item in self.items if item],  # List of item names, skip None
            'reviews': [review.comment for review in self.reviews]
        }

    def __repr__(self):
        return f'<Customer {self.id}, {self.name}>'


# Item Model
class Item(db.Model, SerializerMixin):
    __tablename__ = 'items'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    price = db.Column(db.Float)
    serialize_rules = ('-reviews',)
    def to_dict(self):
        return {
            'id': self.id,
            'name': self.name,
            'price': self.price,
            'reviews': [review.comment for review in self.reviews]
        }
    def __repr__(self):
        return f'<Item {self.id}, {self.name}, {self.price}>'