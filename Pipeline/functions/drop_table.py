from flask_mysqldb import MySQL

# Drop the Database table
def drop_db(app,mysql):
    with app.app_context():
        cursor = mysql.connection.cursor()
        cursor.execute("DROP TABLE IF EXISTS user_input")
        mysql.connection.commit()
        cursor.close()