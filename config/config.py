class Config:
    # Main Database Configuration
    SQLALCHEMY_DATABASE_URI = 'postgresql://<username>:<password>@<host>:<port>/<database_name>'

    # Bind for Additional Databases (e.g., Static Database)
    SQLALCHEMY_BINDS = {
        'static_db': 'postgresql://<username>:<password>@<host>:<port>/<database_name>'
    }

    # Security Keys
    SECRET_KEY = '<your-secret-key>'
    CSRFTOKEN = '<your-csrf-token>'
    JWT_SECRET_KEY = '<your-jwt-secret-key>'
    SALT = '<your-salt>'

    # SQLAlchemy Configuration
    SQLALCHEMY_TRACK_MODIFICATIONS = False

    # Mail Server Configuration
    MAIL_SERVER = '<your-mail-server>'
    MAIL_PORT = 587  # Default for TLS
    MAIL_USERNAME = '<your-email>'
    MAIL_PASSWORD = '<your-email-password>'
    MAIL_USE_TLS = True
    MAIL_USE_SSL = False

    # Additional Configurations
    TESTING = False
