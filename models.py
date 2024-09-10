from db_init import db


class DressModel(db.Model):
    __tablename__ = 'dress'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(200))
    price = db.Column(db.Integer)
    image = db.Column(db.String(300))
    dresses = db.relationship('AddCart', backref='dress', lazy=True)


class AddCart(db.Model):
    __tablename__ = 'add_cart'
    cart_id = db.Column(db.Integer, primary_key=True, autoincrement=True)
    cart = db.Column(db.Integer, db.ForeignKey('dress.id'), nullable=False)
