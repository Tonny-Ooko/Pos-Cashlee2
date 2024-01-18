class Config:
    # Database configuration
    DATABASE_USER = 'root'
    DATABASE_PASSWORD = '123456'
    DATABASE_HOST = 'localhost'
    DATABASE_PORT = '3306'
    DATABASE_NAME = 'users'

    # SQLAlchemy database URI
    SQLALCHEMY_DATABASE_URI = f"mysql://{DATABASE_USER}:{DATABASE_PASSWORD}@{DATABASE_HOST}:{DATABASE_PORT}/{DATABASE_NAME}"

    # Secret key for session management
    SECRET_KEY = "12230tonnyOoko^%$3"
    # Debug mode (should be False in production)
    DEBUG = True
