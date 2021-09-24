import streamlit as st
import pandas as pd
import numpy as np
import requests
import sqlite3
from datetime import datetime
import time
from PIL import Image

#The four models - names for start_model: 'question_answering', 'text_generator', 'sentiment_analysis', 'image_classifier'

def sentiment_analysis(response):
    p = requests.post(url="http://127.0.0.1:8000/sentiment_analysis/",json={"context": response})
    sentiment_label = p.json()["sentiment_label"]
    score = p.json()["score"]
    return sentiment_label, score

def question_answering(response1, response2):
    p= requests.post(url= "http://127.0.0.1:8000/qa/",json= {"context" : response1, "question" : response2})
    answer= p.json()["answer"]
    score= p.json()["score"]
    return answer, score
    
def text_generator(respons):
    pass
def image_classifier(files):
        response = requests.post(url="http://127.0.0.1:8000/classify_image/",files=files)
        result = (response.json())
        return result

def start_model(response):
    with st.spinner(f"Please wait while loading the **{response.replace('_',' ').capitalize()}** model."):
        time.sleep(1)
        requests.post(url="http://127.0.0.1:8000/start/",json={"name":response})
        st.session_state['model_running']=response

def file_namer(img_name): #changing streamlite upload filename blablabal to only filename
    img_name = file_upload
    img_name = str(file_upload)
    img_name_start = img_name.find("name=")+6
    img_name_end = img_name.find("type")-3
    file_name = img_name[img_name_start:img_name_end]
    return file_name

def sql_image_input(img_name,result):
    file_name = file_namer(img_name)
    now = datetime.now()
    dict_keys = [*result.keys()]
    dict_values = [*result.values()]
    data = (now, file_name, dict_keys[0], dict_values[0],dict_keys[1], dict_values[1],dict_keys[2], dict_values[2])
    db = sqlite3.connect('databas.db')
    cur = db.cursor()
    cur.execute(""" Create TABLE IF NOT EXISTS image_classifier
                (input_time integer,image_name text, label_1 text, score_1 real, label_2 text, score_2 real, label_3 text, score_3 real)""")
    cur.execute(" INSERT INTO image_classifier VALUES (?,?,?,?,?,?,?,?)",data)
    db.commit()
    
def sql_img_output(): 
    db = sqlite3.connect("databas.db")
    cur = db.cursor()
    cur.execute(""" Create TABLE IF NOT EXISTS image_classifier
                (input_time integer, label_1 text, score_1 real, label_2 text, score_2 real, label_3 text, score_3 real)""")   
    df = pd.read_sql_query("SELECT * FROM image_classifier", db)
    st.dataframe(df)

def sql_input(text_input, sentiment_output, score_output, validation): #göra modellen öppen för alla modellerna och inte enbart sentiment_analysis
    db = sqlite3.connect('databas.db')
    cur = db.cursor()
    now = datetime.now()
    data = (now, text_input, sentiment_output, score_output, validation)
    cur.execute(" Create TABLE IF NOT EXISTS sentiment_analysis(input_time, input text, sentiment_respons text, score interger, validation text)")
    cur.execute(" INSERT INTO sentiment_analysis VALUES (?,?,?,?,?)",data)
    db.commit()

def sql_output(): 
    db = sqlite3.connect("databas.db")
    cur = db.cursor()
    cur.execute(" Create TABLE IF NOT EXISTS sentiment_analysis(input_time, input text, sentiment_respons text, score interger, validation text)")    
    df = pd.read_sql_query("SELECT * FROM sentiment_analysis", db)
    st.dataframe(df)

def sql_input_qa(context_input, question_input, answer_output, score_output):
    db = sqlite3.connect('databas.db')
    cur = db.cursor()
    now = datetime.now()
    data = (now,context_input, question_input, answer_output, score_output )
    cur.execute(" Create TABLE IF NOT EXISTS question_answer (input_time, context text, question text, answer text, score interger)")
    cur.execute(" INSERT INTO question_answer VALUES (?,?,?,?,?)",data)
    db.commit()

def sql_output_qa():
    db = sqlite3.connect("databas.db")
    cur = db.cursor()
    cur.execute(" Create TABLE IF NOT EXISTS question_answer (input_time, context text, question text, answer text, score interger)")   
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

#---------------
if "model_running" not in st.session_state:
        st.session_state['model_running']="not_activated"
#---------------
option_c = "question_answering"
option_b = "text_generator"
option_a = "sentiment_analysis"
option_d = "image_classifier"
response = ""

st.sidebar.header("Analyzing app")
st.text("")

model_choice = st.sidebar.selectbox("Choose your model",
                            [option_a, option_b, option_c, option_d])

if model_choice!=st.session_state['model_running']:
        start_model(model_choice)

st.text("")
st.markdown(f"### {model_choice.replace('_',' ').capitalize()}")


if model_choice=="question_answering":
    form = st.form(key ="my_form")
    context_input = form.text_input("Write something here."," ")
    question_input = form.text_input("Write a question."," ")
    submit_button=form.form_submit_button(label ="Press when done")
    answer_output, score_output =question_answering(context_input, question_input)
    st.success(f"Answer to your question is : {answer_output} with a surety of {score_output:.4f} ")
    st.text("")
    if st.button('Press to save data'):
        sql_input_qa(context_input, question_input, answer_output, score_output)
    st.text("")
    if st.button('Press to show data'):
        sql_output_qa()

            
elif model_choice=="sentiment_analysis":
    text_input = st.text_input("Write a sentence.","")
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
    pass
elif model_choice=="image_classifier":
    st.write("This model takes your input image and compare it to three labels and gives a score how much the model think your image looks like the label")
    st.write("_You can use the default labels or choose three of your own in the meny._")
 
    file_upload = st.file_uploader("Upload a file", type=["jpeg","jpg","png"])
    
    change_labels = labels_changer()
    
    if file_upload is not None:
        img = Image.open(file_upload)
        files = {'file': file_upload.getvalue()} #the picture as binary
        x = 0
        try:
            result = image_classifier(files)
            st.image(img) #show the users picture
            x=1
        except:
            st.error("The model could not analyse your image please try with another one!")
            x=0 
        if x == 1:
            result = image_classifier(files)
            img_name = file_upload    
            for k, v in result.items():
                result[k] = float(v)
            for key,value in result.items():
                st.write(f"Label: {key} = {value:.6f}")
            if st.button('Press to save data'):
                send_to_sql = sql_image_input(img_name,result)
            if st.button('Press to show data'):
                sql_img_output()
        elif x==0:
            pass
else:
    pass


