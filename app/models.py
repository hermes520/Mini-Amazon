from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app import login



class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True)
    email = db.Column(db.String(120), unique=True)
    password_hash = db.Column(db.String(128))

    def __repr__(self):
        return '<User {}>'.format(self.username)


    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)


@login.user_loader
def load_user(id):
    return User.query.get(int(id))


class Item(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30))
    price = db.Column(db.Float, nullable=False)

    def __repr__(self):
        return '<Item {}>'.format(self.name)

      
class Reviews(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, db.ForeignKey('User.id'))
    item_id = db.Column(db.Integer, primary_key=True, db.ForeignKey('Item.id'))
    date_time = db.Column(db.DateTime, nullable=False, primary_key=True)
    location = db.Column(db.String(120))
    stars = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text)
    comment_thread = db.Column(db.String(1000))

    def __repr__(self):
        return '<Reviews ({}, {}, {}, {}, {}, {}, {})>'.format(self.user_id, self.item_id, self.date_time, self.location, self.stars, self.content, self.comment_thread)

# I think add this to User class
# reviews = db.relationship('Reviews', backref='user_id')

# I think add this to Item class
# reviews = db.relationship('Reviews', backref='item_id')

class SellerReviews(db.Model):
    user_id = db.Column(db.Integer, primary_key=True, db.ForeignKey('User.id'))
    seller_id = db.Column(db.Integer, primary_key=True, db.ForeignKey('Seller.id'))
    date_time = db.Column(db.DateTime, nullable=False, primary_key=True)
    location = db.Column(db.String(120))
    stars = db.Column(db.Integer, nullable=False)
    content = db.Column(db.Text)
    comment_thread = db.Column(db.String(1000))

    def __repr__(self):
        return '<Seller Reviews ({}, {}, {}, {}, {}, {}, {})>'.format(self.user_id, self.seller_id, self.date_time, self.location, self.stars, self.content, self.comment_thread)

# I think add this to User class
# seller_reviews = db.relationship('SellerReviews', backref='user_id')

# I think add this to Seller class
# seller_reviews = db.relationship('SellerReviews', backref='seller_id')

