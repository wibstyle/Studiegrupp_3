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


    if model_choice=="question_answering":
        form = st.form(key ="my_form")
        context_input = form.text_input("Write something here."," ")
        question_input = form.text_input("Write a question."," ")
        submit_button=form.form_submit_button(label ="Press when done")
        answer_output, score_output =question_answering(context_input, question_input)
        if submit_button:
            st.success(f"Answer to your question is : {answer_output} with a surety of {score_output:.4f} ")
            st.text("")
            sql_input_qa(context_input, question_input, answer_output, score_output)
        st.text("")
        if st.button('Press to show data'):
            sql_output_qa()
                
    elif model_choice =="text_generator":

        st.write("This model is not developed in this project.")
        # context_input = st.text_input("Write something to start with....","")
        # if st.button("Tryck"):
        #     answer_output = text_generator(context_input)
        #     st.success(f"Genartated text is: {answer_output} ")
        # if st.button("Save data"):
        #     sql_input_text_generated(context_input, answer_output,)
        # st.text("")
        # if st.button('Press to show data'):
        #     sql_output_text_generated()

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
    elif model_choice=="image_classifier":
        st.write("This model takes your input image and compare it to three labels and gives a score how much the model think your image looks like the label")
        st.write("_You can use the default labels or choose three of your own in the meny._")
    
        file_upload = st.file_uploader("Upload a file", type=["jpeg","jpg","png"])
        
        labels_changer()
        
        if file_upload is not None:
            img = Image.open(file_upload)
            files = {'file': file_upload.getvalue()}    #the picture as binary
            x = 0
            try:
                result = image_classifier(files)
                st.image(img)                           #show the users picture
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
