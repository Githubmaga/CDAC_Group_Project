from flask import request

def submit(mysql):
    if request.method == 'POST':
        input_text = request.form['input_text']
        cursor = mysql.connection.cursor()
        cursor.execute("INSERT INTO user_input (input_text) VALUES (%s)", (input_text,))
        mysql.connection.commit()
        cursor.close()
        return 'Data submitted successfully!'