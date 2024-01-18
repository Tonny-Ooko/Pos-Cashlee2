from flask_login import UserMixin
from passlib.hash import argon2  # Or any other preferred hashing method
# Import NoResultFound from SQLAlchemy's ORM
from .app import (Column,Integer,String,declarative_base,sessionmaker,create_engine
)
from flask import jsonify
# Define a User class to represent user data in your application
class User(UserMixin):
    def __init__(self, id, username, password_hash, role):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role

# Configure your database connection
engine = create_engine('mysql://root:123456@localhost/users')

Base = declarative_base()

class UserInfo(Base):
    __tablename__ = 'user_info'

    id = Column(Integer, primary_key=True)
    username = Column(String(255), unique=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    role = Column(String(50), nullable=False)

# Function to find a user by username
def find_user(username):
    Session = sessionmaker(bind=engine)
    session = Session()

    user_info = session.query(UserInfo).filter(UserInfo.username == username).first()

    if user_info:
        user = User(user_info.id, user_info.username, user_info.password_hash, user_info.role)
        return user
    else:
        return None

# Function to verify a user's password
def verify_password(username, password):
    user = find_user(username)
    if user and argon2.verify(password, user.password_hash):
        return user
    return None
#@app.route('/some_endpoint')
def some_endpoint():
    user = User.query.get(1)  # Replace with your user retrieval logic
    if user is not None:
        return jsonify(user)
    else:
        return jsonify({'message': 'User not found'}), 404