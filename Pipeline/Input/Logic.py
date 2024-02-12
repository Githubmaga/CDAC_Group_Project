from flask import Flask, render_template, request

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
        
        return render_template('index.html', result=classification)
    else:
        return render_template('index.html', result=None)

def preprocess_text(text):
    # Your preprocessing code here (tokenization, cleaning, etc.)
    # Placeholder: return the original text for now
    return text

# Placeholder function for the TensorFlow model
def predict(text):
    # Your TensorFlow model code here
    # Placeholder: random prediction for now
    import random
    return random.choice(["spam", "not spam"])


@app.route('/spam_not_spam')
def spam_non_spam_result():
    return render_template('index.html', spam_text=spam, not_spam_text=non_spam)

if __name__=='__main__':
    app.run(debug=True)