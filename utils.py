import streamlit as st
import pandas as pd
import requests
import sqlite3
from datetime import datetime
import time
from PIL import Image



def sentiment_analysis(response: str)-> str:
    p = requests.post(url="http://127.0.0.1:8000/sentiment_analysis/",json={"context": response})
    sentiment_label = p.json()["sentiment_label"]
    score = p.json()["score"]
    return sentiment_label, score

def question_answering(response1: str, response2: str)-> str:
    p= requests.post(url= "http://127.0.0.1:8000/qa/",json= {"context" : response1, "question" : response2})
    answer= p.json()["answer"]
    score= p.json()["score"]
    return answer, score   

def start_model(response: str):
    with st.spinner(f"Please wait while loading the **{response.replace('_',' ').capitalize()}** model."):
        time.sleep(1)
        requests.post(url="http://127.0.0.1:8000/start/",json={"name":response})
        st.session_state['model_running']=response


    
def sql_img_output(): 
    db = sqlite3.connect("databas.db")
    cur = db.cursor()
    cur.execute(""" CREATE TABLE IF NOT EXISTS image_classifier
                    (input_time integer,image_name text, label_1 text, score_1 real, label_2 text, score_2 real, label_3 text, score_3 real)""")
    df = pd.read_sql_query("SELECT * FROM image_classifier", db)
    st.dataframe(df)

def sql_input(text_input, sentiment_output, score_output, validation): #göra modellen öppen för alla modellerna och inte enbart sentiment_analysis
    db = sqlite3.connect('databas.db')
    cur = db.cursor()
    now = datetime.now()
    data = (now, text_input, sentiment_output, score_output, validation)
    cur.execute(" CREATE TABLE IF NOT EXISTS sentiment_analysis(input_time, input text, sentiment_respons text, score interger, validation text)")
    cur.execute(" INSERT INTO sentiment_analysis VALUES (?,?,?,?,?)",data)
    db.commit()

def sql_output(): 
    db = sqlite3.connect("databas.db")
    cur = db.cursor()
    cur.execute(" CREATE TABLE IF NOT EXISTS sentiment_analysis(input_time, input text, sentiment_respons text, score interger, validation text)")    
    df = pd.read_sql_query("SELECT * FROM sentiment_analysis", db)
    st.dataframe(df)



def sql_output_qa():
    db = sqlite3.connect("databas.db")
    cur = db.cursor()
    cur.execute(" CREATE TABLE IF NOT EXISTS question_answer (input_time, context text, question text, answer text, score interger)")   
    df = pd.read_sql_query("SELECT * FROM question_answer", db)
    st.dataframe(df)       

def labels_changer():
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("Here you can change the labels for the image classifier.default is cat,dog and banana")
    st.sidebar.write("Default value is: _cat,dog and banana_")
    labels = st.sidebar.columns(3)
    first_label = labels[0].text_input("1st label",value="cat",key=1)
    second_label = labels[1].text_input("2nd label",value="dog",key=2)
    third_label = labels[2].text_input("3rd label",value="banana",key=3)
    change_labels = {"class_1": first_label,
        "class_2": second_label,
        "class_3": third_label}
    flag = len(change_labels) != len(set(change_labels.values()))
    if flag == False and change_labels["class_1"] != "" and change_labels["class_2"] != "" and change_labels["class_3"] != "": 
        requests.put(url="http://127.0.0.1:8000/change_classes/",json=change_labels)
    else:
        st.sidebar.error("All labels must have a unique value")


def sql_output_text_generated():
    db = sqlite3.connect("databas.db")
    cur = db.cursor()
    cur.execute(" CREATE TABLE IF NOT EXISTS text_generated(input_time, context text, answer text)")   
    df = pd.read_sql_query("SELECT * FROM text_generated", db)
    st.dataframe(df)

def image_classifier(files):
        response = requests.post(url="http://127.0.0.1:8000/classify_image/",files=files)
        result = (response.json())
        return result
        
def sql_input_qa(context_input, question_input, answer_output, score_output):
    db = sqlite3.connect('databas.db')
    cur = db.cursor()
    now = datetime.now()
    data = (now,context_input, question_input, answer_output, score_output )
    cur.execute(" CREATE TABLE IF NOT EXISTS question_answer (input_time, context text, question text, answer text, score interger)")
    cur.execute(" INSERT INTO question_answer VALUES (?,?,?,?,?)",data)
    db.commit()


#----------------------TO BE DELETED -----------------------------
def text_generator(response):
    p = requests.post(url= "http://127.0.0.1:8000/text_generation/",json= {"context" : response})
    response =p.json()
    generated_text = response['generated_text']
    answer = generated_text[:100]
    return answer

def sql_input_text_generated(context_input, answer_output):
    db = sqlite3.connect('databas.db')
    cur = db.cursor()
    now = datetime.now()
    data = (now, context_input, answer_output )
    cur.execute(" Create TABLE IF NOT EXISTS text_generated(input_time, context text, answer text)")
    cur.execute(" INSERT INTO text_generated VALUES (?,?,?)",data)
    db.commit()
