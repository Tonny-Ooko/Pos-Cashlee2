# auth_module.py
from flask_sqlalchemy import SQLAlchemy
# auth_module.py

db = SQLAlchemy()
class User(db.Model):
    __tablename__ = 'user_info'  # Match the actual table name in your database

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)
    role = db.Column(db.String(50), nullable=False)
    is_active = db.Column(db.Boolean, default=True)  # Add is_active field

