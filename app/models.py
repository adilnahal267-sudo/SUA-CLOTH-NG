from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager

@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))

class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), index=True, unique=True, nullable=False)
    email = db.Column(db.String(120), index=True, unique=True, nullable=False)
    password_hash = db.Column(db.String(128))

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class ClothingItem(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    description = db.Column(db.Text, nullable=True)
    # Relationship to images
    images = db.relationship('ItemImage', backref='item', lazy=True, cascade="all, delete-orphan")
    # Relationship to features
    features = db.relationship('ItemFeature', backref='item', lazy=True, cascade="all, delete-orphan")

class ItemImage(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('clothing_item.id'), nullable=False)
    image_filename = db.Column(db.String(100), nullable=False)
    view_type = db.Column(db.String(20), nullable=False) # 'front', 'back', 'side'

class ItemFeature(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    item_id = db.Column(db.Integer, db.ForeignKey('clothing_item.id'), nullable=False)
    key = db.Column(db.String(50), nullable=False) # e.g., 'color', 'pattern'
    value = db.Column(db.String(50), nullable=False) # e.g., 'blue', 'striped'
