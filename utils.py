import streamlit as st
import pandas as pd
import requests
import sqlite3
from datetime import datetime
import time
from PIL import Image

def file_namer(img_name: str)->str:
    """Extracts the filename that was uploaded

    Args:
        img_name (Streamlit Upload file information): Name retrived from using Streamlit upload function

    Returns:
        file_name (str): Returns the filename and nothing else
    """
    image_name = str(img_name)
    img_name_start = image_name.find("name=")+6
    img_name_end = image_name.find("type")-3
    file_name = image_name[img_name_start:img_name_end]
    return file_name

def sql_image_input(img_name: str,result: str):
    """Save the the data from the Image_classifier model to a SQLite databas, creates database and tables if needed.

    Args:
        img_name (Streamlit Upload file information): [Name retrived from using Streamlit upload function]
        result   (dict) : dict that is sent back from the model Image_classifier
    Returns:
        [none]: [Only input and save nothing is]
    """
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

def sentiment_analysis(response: str)-> str:
    """Sends a request to the Sentiment model. 

    Args:
        response (str): A string to be analysed.

    Returns:
        str: Returns an analysed value(positive or negative) and a score of certainty. 
    """
    p = requests.post(url="http://127.0.0.1:8000/sentiment_analysis/",json={"context": response})
    sentiment_label = p.json()["sentiment_label"]
    score = p.json()["score"]
    return sentiment_label, score

def question_answering(response1: str, response2: str)-> str:
    """Sends a request to the QA-model.

    Args:
        response1 (str): Contains the text to be investigated.
        response2 (str): Contains the question to be answered.

    Returns:
        str: Returns the answer to the question and a score of certainty.
    """
    p= requests.post(url= "http://127.0.0.1:8000/qa/",json= {"context" : response1, "question" : response2})
    answer= p.json()["answer"]
    score= p.json()["score"]
    return answer, score   

def start_model(response: str):
    """This funtions starts the requested model. 
    Also updates sessionState variable to keep trackof which model is running.

    Args:
        response (str): The model to be started.
    """
    with st.spinner(f"Please wait while loading the **{response.replace('_',' ').capitalize()}** model."):
        time.sleep(1)
        requests.post(url="http://127.0.0.1:8000/start/",json={"name":response})
        st.session_state['model_running']=response


    
def sql_img_output():
    """Collects all columns from table image_classifier.
    If table doesnt exist - it's created. Function prints dataframe thru streamlit command.
    
    """
    db = sqlite3.connect("databas.db")
    cur = db.cursor()
    cur.execute(""" CREATE TABLE IF NOT EXISTS image_classifier
                    (   input_time integer,
                        image_name text, 
                        label_1 text, 
                        score_1 real, 
                        label_2 text, 
                        score_2 real, 
                        label_3 text, 
                        score_3 real)""")
    df = pd.read_sql_query("SELECT * FROM image_classifier", db)
    st.dataframe(df)

def sentimental_analysis_sql_output():
    """ This function collects data from all columns and returns all rows from table(sentiment_analysis).
        This table is connected to the Sentiment-model.
    """
    db = sqlite3.connect("databas.db")
    cur = db.cursor()
    cur.execute(" CREATE TABLE IF NOT EXISTS sentiment_analysis(input_time, input text, sentiment_respons text, score interger, validation text)")    
    df = pd.read_sql_query("SELECT * FROM sentiment_analysis", db)
    st.dataframe(df)

def sql_output_qa():
    """ This function collects data from all columns and returns all rows from table(question_answer).
        This table is connected to the QA-model.
    """
    db = sqlite3.connect("databas.db")
    cur = db.cursor()
    cur.execute(" CREATE TABLE IF NOT EXISTS question_answer (input_time, context text, question text, answer text, score interger)")   
    df = pd.read_sql_query("SELECT * FROM question_answer", db)
    st.dataframe(df)       

def refresh_category():
    """Setting state varaiable to 1. (Kind of silly but necessary to be able to work with on_change event for widget)
    """
    st.session_state['cat']=1

def init_session_state_image_classifier():
    """ This method initialize two session state variables.
        cat:                keeps track of any changes been made in categories. Only call API when its necessary
        hide_upload_panel:  if user put empty boxes in categories -> dont show upload widget
    """ 
    if "cat" not in st.session_state:
        st.session_state['cat']=0                   # 0 = zero changes made in categories
    if "hide_upload_panel" not in st.session_state:
        st.session_state['hide_upload_panel']=0     # 0 = show upload panel, 1 = hide upload panel

def labels_changer():
    """ The image classifier are analysing an image against three cathegories(labels).
        This fuctions collects values from three text inputs and update the labels via the API connected 
        to the image classifier.
    """
    st.sidebar.write("")
    st.sidebar.write("")
    st.sidebar.write("Here you can change the labels for the image classifier.default is cat,dog and banana")
    st.sidebar.write("Default value is: _cat,dog and banana_")
    labels = st.sidebar.columns(3)
    first_label = labels[0].text_input("1st label",value="cat",key=1, on_change= refresh_category)
    second_label = labels[1].text_input("2nd label",value="dog",key=2, on_change= refresh_category)
    third_label = labels[2].text_input("3rd label",value="banana",key=3, on_change= refresh_category)
    change_labels = {"class_1": first_label,
        "class_2": second_label,
        "class_3": third_label}
    flag = len(change_labels) != len(set(change_labels.values()))
    if st.session_state['cat']==1:                                      # check if any category been modified
        if flag == False and change_labels["class_1"] != "" and change_labels["class_2"] != "" and change_labels["class_3"] != "": 
            requests.put(url="http://127.0.0.1:8000/change_classes/",json=change_labels)
            st.session_state['cat']=0
            st.session_state['hide_upload_panel']=0                     # everything is good -> show upload panel
            
        else:
            st.sidebar.error("All labels must have a unique value")
            st.session_state['hide_upload_panel']=1                     # something is wrong with categories -> hide upload panel
            
        

def image_classifier(files):
    """Sends a request to the Image_classifier model. 

    Args:
        response (array): the input image from the user, in binary code

    Returns:
        result (dict): Returns three analysed values based on how much the picture looks like the model. 
    """
    response = requests.post(url="http://127.0.0.1:8000/classify_image/",files=files)
    result = (response.json())
    return result
        
def sql_input_qa(context_input:str, question_input:str, answer_output:str, score_output: float):
    """Save the the data from the QA model to a SQLite databas, creates database and tables if needed.

    Args:
        context_input (str): The frase from with we want to the test model against. 
        question_input (str): The question related to the frase in context_input
        answer_output (str): The output answer from the model
        score_output (float): The score from the model
    """
    db = sqlite3.connect('databas.db')
    cur = db.cursor()
    now = datetime.now()
    data = (now,context_input, question_input, answer_output, score_output )
    cur.execute(" CREATE TABLE IF NOT EXISTS question_answer (input_time, context text, question text, answer text, score interger)")
    cur.execute(" INSERT INTO question_answer VALUES (?,?,?,?,?)",data)
    db.commit()

def sentimental_analysis_sql_input(text_input, sentiment_output, score_output, validation): #g??ra modellen ??ppen f??r alla modellerna och inte enbart sentiment_analysis
    """Save the the data from the sentiment analysis model to a SQLite databas, creates database and tables if needed.

    Args:
        text_input ([str]): the input data from the user that is analysed  
        sentiment_output ([type]): the respons from the model
        score_output ([type]): the respons score from the model
        validation ([type]): the user is able to give input if the sentiment analysis is what they though it would be
    """
    db = sqlite3.connect('databas.db')
    cur = db.cursor()
    now = datetime.now()
    data = (now, text_input, sentiment_output, score_output, validation)
    cur.execute(" CREATE TABLE IF NOT EXISTS sentiment_analysis(input_time, input text, sentiment_respons text, score interger, validation text)")
    cur.execute(" INSERT INTO sentiment_analysis VALUES (?,?,?,?,?)",data)
    db.commit()

