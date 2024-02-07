import os


def Database_config(app):
    app.config['MYSQL_HOST'] = os.environ.get('MYSQL_HOST', 'localhost')
    app.config['MYSQL_USER'] = os.environ.get('MYSQL_USER', 'root')
    app.config['MYSQL_PASSWORD'] = os.environ.get('MYSQL_PASSWORD', 'password')
    app.config['MYSQL_DB'] = os.environ.get('MYSQL_DB', 'your_database_name')
    app.config['SECRET_KEY'] = os.environ.get('SECRET_KEY', 'your_secret_key')