from flask import Flask, render_template, request,redirect,url_for
from gensim.models import Word2Vec
from gensim.utils import simple_preprocess
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow import keras
import joblib
import torch
from transformers import pipeline
from sumy.summarizers.lex_rank import LexRankSummarizer
from sumy.parsers.plaintext import PlaintextParser
from sumy.nlp.tokenizers import Tokenizer
from transformers import RobertaTokenizer, RobertaForSequenceClassification
import torch

app=Flask(__name__,static_folder='static')

spam_list=[]
non_spam_list=[]
positives=[]
negatives=[]

word2vec_model=Word2Vec.load('D:\CDAC_PUNE_PROJECT\CDAC_Group_Project\Pipeline\Input\word2vec_model.bin')

model = keras.models.load_model('D:\CDAC_PUNE_PROJECT\CDAC_Group_Project\Pipeline\Input\lstm_model4.h5')

'''
model_path = 'D:\Cdac group project\Pipeline2\Input\pytorchmodel.bin'
roberta_model = RobertaForSequenceClassification.from_pretrained(model_path)
tokenizer = RobertaTokenizer.from_pretrained(model_path)
'''



def sentiment_analyzer(text):
    sentimental_model=pipeline('sentiment-analysis')
    res = sentimental_model(text)
    sent=res[0].get('label')
    if sent=='POSITIVE':
        positives.append(text)
    else:
        negatives.append(text)    

def sentiment_analyzer2(text):
    inputs = tokenizer(text, return_tensors='pt', truncation=True, padding=True)
    outputs = model(**inputs)
    predicted_class = torch.argmax(outputs.logits).item()
    sentiment_label = "Positive" if predicted_class == 1 else "Negative"
    if sentiment_label=='Positive':
        positives.append(text)
    else:
        negatives.append(text)  


def clean_text_for_prediction(sent):
    sent_list=simple_preprocess(sent)
    sequence = []
    for word in sent_list:
        if word in word2vec_model.wv:
            sequence.append(word2vec_model.wv.key_to_index[word])
    return sequence

@app.route('/', methods=['GET', 'POST'])
def index():
    global text
    if request.method == 'POST':
        text = request.form['text']
        classification = classify(text)
        
        if classification == 'spam':
            spam_list.append(text)
        elif classification=='not spam':
            non_spam_list.append(text)
        
        return render_template('Home.html', result=classification)
    else:
        return render_template('Home.html', result=None)

def classify(text):
    # Transform input text using TF-IDF Vectorizer
    sent_seq = clean_text_for_prediction(text)
    max_sequence_length=300
    padded_sequences = pad_sequences([sent_seq], maxlen=max_sequence_length, padding='post')
    # Predict using SVM Classifier
    prediction = model.predict(padded_sequences)
    
    # Convert prediction to human-readable form
    if prediction > 0.9:
        return 'spam'
    else:
        return 'not spam'
    
@app.route('/spam_not_spam')
def spam_not_spam():
    return render_template('spam_not_spam.html',spam_text=spam_list, not_spam_text=non_spam_list)

summary_list=[]
@app.route('/summary') 
def summary():
    summary_sent=''
    text=' '.join(non_spam_list)
    parser = PlaintextParser.from_string(text,Tokenizer('english'))
    lex_rank_summarizer=LexRankSummarizer()
    summary=lex_rank_summarizer(parser.document,sentences_count=5)
    for sent in summary:
        sent=str(sent)
        summary_sent=summary_sent + sent
    
    #sentiment Analysis
    for lines in non_spam_list:
        sentiment_analyzer(lines) 
    return render_template('summary_pos_neg.html',summary=summary_list,positive_reviews=positives,negative_reviews=negatives,summary_sentences=summary_sent)


if __name__=='__main__':
    app.run(debug=True)