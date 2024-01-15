from flask import Flask, render_template, request
from functions import submit_input,database_configurations,drop_table,initialize_db
from flask_mysqldb import MySQL

app=Flask(__name__)

database_configurations.Database_config(app)

mysql=MySQL(app)

@app.before_first_request
def before_first_request():
    drop_table()
    initialize_db()


@app.route('/',methods=['POST','GET'])
def input_text():
    if request.method=='POST':
        user_input=request.form['user_input']
        print(f'user input is {user_input}')
        submit_input.submit()
    return render_template('Home.html')



if __name__=='__main__':
    app.run(debug=True)