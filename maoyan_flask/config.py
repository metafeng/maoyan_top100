import os
DEBUG = 1
# dialect+driver://username:password@host:port/database
DIALECT = 'mysql'
DRIVER = 'pymysql'
HOST = os.getenv("MYSQL_HOST") if os.getenv("MYSQL_HOST") else '127.0.0.1'
USERNAME = os.getenv("MYSQL_USERNAME") \
    if os.getenv("MYSQL_USERNAME") else 'username'
PASSWORD = os.getenv("MYSQL_PASSWORD") \
    if os.getenv("MYSQL_PASSWORD") else 'password'
PORT = os.getenv("MYSQL_PORT") \
    if os.getenv("MYSQL_PORT") else 3306
DATABASE = 'maoyan_flask'


SQLALCHEMY_DATABASE_URI = \
    f"{DIALECT}+{DRIVER}://{USERNAME}:{PASSWORD}@{HOST}:{PORT}/{DATABASE}\
?charset=utf8"
SQLALCHEMY_TRACK_MODIFICATIONS = False
