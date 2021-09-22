#from utils import useless_method2
#from utils import useless_method

import pandas as pd
import matplotlib.pyplot as plt
from requests.sessions import session
from streamlit.state.session_state import SessionState 
import ml_models2
import dbHandler
import streamlit as st
from PIL import Image



def main():
    db_obj = dbHandler.DatabaseHandlerClass()
    sentiment_obj = ml_models2.ML_ModelClass()
    sentiment_obj.analyse_model_check()
    
    
    lst=["Try phrase","View history", "See data"]    
    val=st.sidebar.selectbox("",lst)
    
    if val=="Try phrase":
        st.write("# Let me analyze your favourite phrase!")
        text_inp=st.text_input("Enter phrase:","")
        if text_inp:
            sentiment_obj.send_for_analyze(text_inp) 
            db_obj.write_row(sentiment_obj.phrase, sentiment_obj.sentiment_response, sentiment_obj.score )   
            sentiment_obj.stream_print()
    
    if val=="View history":
        st.write("some history text")
        
        image_unicorn = "unicorn.jpg"
        image_lego = "lego-wizard.jpg"
        unicorn = Image.open(image_unicorn)
        lego_wizard = Image.open(image_lego)
        
        col1, col2 = st.columns(2)
        with col1:
            st.header("Unicorn")
            st.image(unicorn, use_column_width=True)

        with col2:
            st.header("Wizard")
            st.image(lego_wizard, use_column_width=True)
            
        phrase_list = db_obj.get_all_phrases()    
        stored_selectbox2 = st.selectbox('View stored phrase:', phrase_list, key="sele")
        
        sentiment_obj.send_for_analyze(stored_selectbox2)   
        sentiment_obj.stream_print()

    if val=="See data":
        st.header("Plot view")
        df = db_obj.return_df()
        st.bar_chart(df)

if __name__=="__main__":
    main()