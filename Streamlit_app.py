import streamlit as st
import pandas as pd
import numpy as np
import requests
import sqlite3
from sqlite3 import Cursor
from datetime import datetime
import time


st.title("Have some instant fun!!")
st.markdown("Here you get an instant response about how you feel by just sharing what's on your mind.")
col1, col2 =st.columns(2)
with col2:
    st.subheader('Enter your name')
    user_name = st.text_input("")
    st.markdown(f"Nice to meet you: {user_name}")
with col1:
    st.header('Welcome')
    image_url = ("Thinking emoji.png")
    st.image(image_url, width = 300)
#user_name = st.text_input("Enter you name.", "")
#st.markdown(f"Nice to meet you: {user_name}")

def view_as_table():
    db = sqlite3.connect('database.db')
    cur = db.cursor()
    cur.execute('''CREATE TABLE IF NOT EXISTS sentiment_analysis(
                Name,
                Feelings,
                Result,
                Score,
                )''')
    
    cur.execute(" INSERT INTO sentiment_analysis VALUES (?,?,?,?)",data)
    db.commit()


  

def sentiment_analysis(text_input):
    r = requests.post(url= "http://127.0.0.1:8000/start/", json={"name":"sentiment_analysis"})
    p= requests.post(url= "http://127.0.0.1:8000/sentiment_analysis/",json= {"context":text_input})
    sentiment_label = p.json()["sentiment_label"]
    score = p.json()["score"]
    return sentiment_label, score

#with st.form(key ='my_form'):
    user_name = st.text_input(label='Enter your name')
    submit_button = st.form_submit_button(label ='Submit')
    if submit_button:
        st.write(f'Hello {user_name}')

if st.checkbox('Are you ready'):
    
    text_input=st.text_input("Write something on your mind just now..")
    if st.button("Click here when you are done"):
        my_bar=st.progress(0)
        sentiment_output, score_output = sentiment_analysis(text_input)
        for percent_complete in range(100):
            time.sleep(0.1)
            my_bar.progress(percent_complete + 1)
        
        if sentiment_output.capitalize() == "Positive":
            st.success(f"Sentiment response: {sentiment_output.capitalize()} at a score rate of {score_output:.4f}")
            time.sleep(2)
            st.balloons()
        elif sentiment_output.capitalize() == "Negative":

            st.error(f"Sentiment response: {sentiment_output.capitalize()} at a score rate of {score_output:.4f}")
        
        if st.button("Save result"):
            db = sqlite3.connect('database.db')
            cur = db.cursor()
            cur.execute('''CREATE TABLE IF NOT EXISTS sentiment_analysis(
                        Name,
                        Feelings,
                        Result,
                        Score,
                        )''')
            data = (user_name, text_input, sentiment_output, sentiment_output)
            cur.execute(f"INSERT INTO history VALUES(?,?,?,?)", data)
            db.commit()
        
        if st.checkbox("View as Table"):
            cur.execute("SELECT FROM history WHERE Name = 'user_name' ")
            st.dataframe(cur.fetchall())
            df = pd.read(st.dataframe)
            print(df)
        
        #if st.checkbox("View as Table"):
        # sql_input(user_name, text_input, sentiment_output, score_output)
        #sql_output()
    



    







 
