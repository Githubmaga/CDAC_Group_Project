from flask import Flask, render_template, request
import joblib
app=Flask(__name__)

spam_list=[]
non_spam_list=[]

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        text = request.form['text']
        processed_text = preprocess_text(text)
        classification = predict(processed_text)
        
        if classification == 'spam':
            spam_list.append(text)
        else:
            non_spam_list.append(text)
        
        return render_template('Home.html', result=classification)
    else:
        return render_template('Home.html', result=None)

def preprocess_text(text):
    model=joblib.load('CDAC_Group_Project\Pipeline\Input\tfidf_vectorizer.joblib')
    model.predict()
    return text

# Placeholder function for the TensorFlow model
def predict(text):
    # Your TensorFlow model code here
    # Placeholder: random prediction for now
    import random
    return random.choice(["spam", "not spam"])


@app.route('/spam_not_spam')
def spam_non_spam_result():
    return render_template('spam_not_spam.html', spam_text=spam_list, not_spam_text=non_spam_list)

if __name__=='__main__':
    app.run(debug=True)