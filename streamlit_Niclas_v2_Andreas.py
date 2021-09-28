import streamlit as st
import pandas as pd
import requests
import sqlite3
from datetime import datetime
import time
from PIL import Image
from utils import *

def main():

    #---------------
    if "model_running" not in st.session_state:
            st.session_state['model_running']="not_activated"
    #---------------

    option_c = "question_answering"
    option_b = "text_generator"
    option_a = "sentiment_analysis"
    option_d = "image_classifier"

    st.sidebar.header("Analyzing app")
    st.text("")

    model_choice = st.sidebar.selectbox("Choose your model",
                                [option_a, option_b, option_c, option_d])

    if model_choice!=st.session_state['model_running']:
            start_model(model_choice)

    st.text("")
    st.markdown(f"### {model_choice.replace('_',' ').capitalize()}")

#---------------------------------------------
    if model_choice=="question_answering":
        form = st.form(key ="my_form")
        context_input = form.text_input("Write something here."," ")
        question_input = form.text_input("Write a question."," ")
        submit_button=form.form_submit_button(label ="Press when done")
        if submit_button:
            if len(context_input)>2 and len(question_input)>2:
                answer_output, score_output =question_answering(context_input, question_input)
                st.success(f"Answer to your question is : {answer_output} with a surety of {score_output:.4f} ")
                st.text("")
                sql_input_qa(context_input, question_input, answer_output, score_output)
            else:
                st.error("Both fields must have a value.")        
        st.text("")
        if st.button('Press to show data'):
            sql_output_qa()

#---------------------------------------------                
    elif model_choice =="text_generator":

        st.write("This model is not developed in this project.")
#---------------------------------------------
    elif model_choice=="sentiment_analysis":
        text_input = st.text_input("Write a sentence.","")
        sentiment_output, score_output = sentiment_analysis(text_input)
        if text_input:
            if sentiment_output.capitalize() == "Positive":
                st.success(f"Sentiment response: {sentiment_output.capitalize()} at a score rate of {score_output:.4f}")
            elif sentiment_output.capitalize() == "Negative":
                st.error(f"Sentiment response: {sentiment_output.capitalize()} at a score rate of {score_output:.4f}")
            st.text("")
            st.markdown('** Do you agree? Please respond below **')
            validation = st.selectbox("",["Positive","Negative"])
            
            if st.button('Press to save data'):
                sentimental_analysis_sql_input(text_input, sentiment_output, score_output, validation.upper())
            st.text("")
            st.text("")
            if st.button('Press to show data'):
                sentimental_analysis_sql_output()
            pass

#---------------------------------------------
    elif model_choice=="image_classifier":
        init_session_state_image_classifier()                       # initialize cat and hide_panel (session state variables)
        
        st.write("This model takes your input image and compare it to three labels and gives a score how much the model think your image looks like the label")
        st.write("_You can use the default labels or choose three of your own in the meny._")
        labels_changer()
        
        if st.session_state['hide_upload_panel']==0:                # if somethin is wrong with categories -> hide panel
            file_upload = st.file_uploader("Upload a file", type=["jpeg","jpg","png"])
        
            if file_upload is not None: #and st.session_state['show_error']==1:
                img = Image.open(file_upload)
                files = {'file': file_upload.getvalue()}            #the picture as binary
                x = 0
                try:
                    result = image_classifier(files)
                    st.image(img)                                   #show the users picture
                    x=1
                except ValueError:
                    st.error("The model could not analyse your image please try with another one!")
                    x=0 
                if x == 1:
                    img_name = file_upload    
                    for k, v in result.items():
                        result[k] = float(v)
                    for key,value in result.items():
                        st.write(f"Label: {key} = {value:.6f}")
                    if st.button('Press to save data'):
                        sql_image_input(img_name,result)
                    if st.button('Press to show data'):
                        sql_img_output()
                elif x==0:
                    pass
    else:
        pass



if __name__=="__main__":
    main()
