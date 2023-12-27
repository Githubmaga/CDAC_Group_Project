from flask import Flask, render_template, request
app=Flask(__name__)

@app.route('/login',methods=['POST','GET'])
def input_text():
    if request.method=='POST':
        user_input=request.form['user_input']
        print(f'user input is {user_input}')
    
    return render_template('Home.html')



if __name__=='__main__':
    app.run(debug=True)