from flask_mysqldb import MySQL
from drop_table import drop_db
from create_table import create_table

#Initalize the DataBase
def init(app,mysql):
    drop_db(app,mysql)
    create_table(app,mysql)


