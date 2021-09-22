import streamlit as st
import pandas as pd
import numpy as np
import requests
import sqlite3
from datetime import datetime
import time
from PIL import Image


def sentiment_analysis(response):
    p = requests.post(url="http://127.0.0.1:8000/sentiment_analysis/",json={"context": response})
    sentiment_label = p.json()["sentiment_label"]
    score = p.json()["score"]
    return sentiment_label, score



def start_model(response):
    with st.spinner('Loading model...'):
        time.sleep(1)
        requests.post(url="http://127.0.0.1:8000/start/",json={"name":response})
        st.success(f"Done! {response.replace('_',' ').capitalize()} has been loaded!")
    
    #'question_answering', 'text_generator', 'sentiment_analysis', 'image_classifier'
    pass

def sql_input(text_input, sentiment_output, score_output, validation): #göra modellen öppen för alla modellerna och inte enbart sentiment_analysis
    db = sqlite3.connect('databas.db')
    cur = db.cursor()
    now = datetime.now()
    data = (text_input, sentiment_output, score_output, validation, now)
    cur.execute(" INSERT INTO sentiment_analysis VALUES (?,?,?,?,?)",data)
    db.commit()

def sql_output(): #behöver fixa en Try Catch om databas.db inte finns. Göra den öppen för alla modellerna och inte enbart sentiment_analysis
    conn = sqlite3.connect("databas.db")
    df = pd.read_sql_query("SELECT * FROM sentiment_analysis", conn)
    st.dataframe(df)


option_a = "question_answering"
option_b = "text_generator"
option_c = "sentiment_analysis"
option_d = "image_classifier"
response = ""

st.sidebar.header("Analyzing app")
st.text("")

check_if_loaded = {"question_answering":0,"text_generator":0,"sentiment_analysis":0,"image_classifier":0} #dict över modellerna och värde på vilken modell som är laddad eller inte

model_choice = st.sidebar.selectbox("Choose your model",
                            [option_a, option_b, option_c, option_d])
if st.sidebar.button('Press to load model'):
    start_model(model_choice)
    for key, value in check_if_loaded.items(): # tömmer värdet på dict så att alla är 0
        value = 0 
    check_if_loaded[model_choice] = 1 #lägger till värdet 1 i den dict som är laddad
    

st.text("")
st.markdown(f"### {model_choice.replace('_',' ').capitalize()}")



if check_if_loaded[model_choice] == 1: #kollar om modellens värde är 1 i dict check_if_loaded annars skall inget skrivas ut
    context_input = st.text_input("Write a sentence."," ")
    question_inpu = st.text_input("Write a question."," ")
elif check_if_loaded[model_choice] == 1:#kollar om modellens värde är 1 i dict check_if_loaded annars skall inget skrivas ut
    pass
elif check_if_loaded[model_choice]==1:#kollar om modellens värde är 1 i dict check_if_loaded annars skall inget skrivas ut
    text_input = st.text_input("Write a sentence."," ")
    sentiment_output, score_output = sentiment_analysis(text_input)
    if sentiment_output.capitalize() == "Positive":
        st.success(f"Sentiment response: {sentiment_output.capitalize()} at a score rate of {score_output:.4f}")
    elif sentiment_output.capitalize() == "Negative":
        st.error(f"Sentiment response: {sentiment_output.capitalize()} at a score rate of {score_output:.4f}")
    st.text("")
    st.markdown('** Do you agree? Please respond below **')
    validation = st.selectbox("",["Positive","Negative"])
    if st.button('Press to save data'):
        sql_input(text_input, sentiment_output, score_output, validation.upper())
    st.text("")
    st.text("")
    if st.button('Press to show data'):
        sql_output()
    
elif check_if_loaded[model_choice]==1:#kollar om modellens värde är 1 i dict check_if_loaded annars skall inget skrivas ut
    pass
else:
    pass


