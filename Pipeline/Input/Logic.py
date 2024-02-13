from flask import Flask, render_template, request,redirect,url_for

import joblib

app=Flask(__name__)

spam_list=[]
non_spam_list=[]
tfidf_model=joblib.load('D:/CDAC_PUNE_PROJECT/CDAC_Group_Project/Pipeline/Input/vectorizer.joblib')
svm_model = joblib.load('D:/CDAC_PUNE_PROJECT/CDAC_Group_Project/Pipeline/Input/SVM_Classifier_03(RBF_Kernel).joblib')

@app.route('/', methods=['GET', 'POST'])
def index():
    global text
    if request.method == 'POST':
        text = request.form['text']
        classification = classify(text)
        
        if classification == 'spam':
            spam_list.append(text)
        else:
            non_spam_list.append(text)
        
        return render_template('Home.html', result=classification)
    else:
        return render_template('Home.html', result=None)

def classify(text):
    # Transform input text using TF-IDF Vectorizer
    text_vectorized = tfidf_model.transform([text])
    
    # Predict using SVM Classifier
    prediction = svm_model.predict(text_vectorized)
    
    # Convert prediction to human-readable form
    if prediction == 1:
        return 'spam'
    else:
        return 'not spam'

def clean_text(sent):
    token1 = word_tokenize(sent) #tokenizing the sentences
    #token2 = [x.lower() for x in token1 if x not in string.punctuation] #Removing the punctuations
    token2 = [x.lower() for x in token1 if x.isalpha() or x.isdigit()] #Removing the punctuations
    token3 = [ls.lemmatize(x) for x in token2 if x not in stopwords] #removing affixes
    return token3 

@app.route('/spam_not_spam')
def spam_not_spam():
    return render_template('spam_not_spam.html',spam_text=spam_list, not_spam_text=non_spam_list)

if __name__=='__main__':
    app.run(debug=True)