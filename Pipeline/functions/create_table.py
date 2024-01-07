from flask_mysqldb import MySQL

def create_table(app,mysql):
        with app.app_context():
              cursor = mysql.connection.cursor()
              cursor.execute("""
                             CREATE TABLE IF NOT EXISTS user_input (
                             id INT AUTO_INCREMENT PRIMARY KEY,
                             input_text VARCHAR(255)
                             )
                             """)
              mysql.connection.commit()
              cursor.close()
