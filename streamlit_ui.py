#from utils import meanless_method2
#from utils import meanless_method

import pandas as pd
import matplotlib.pyplot as plt 
import ml_models2
import dbHandler
import streamlit as st
from PIL import Image

def main():
    
    db_obj = dbHandler.DatabaseHandlerClass()
    sentiment_obj = ml_models2.ML_ModelClass()
    sentiment_obj.analyse_model_check()
    
    image_unicorn = "unicorn.jpg"
    image_lego = "lego-wizard.jpg"
    unicorn = Image.open(image_unicorn)
    lego_wizard = Image.open(image_lego)
    st.write("# Let me analyze your favourite phrase!")
    col1, col2 = st.columns(2)

    col1.header("Unicorn")
    col1.image(unicorn, use_column_width=True)

    col2.header("Wizard")
    col2.image(lego_wizard, use_column_width=True)

    
    phrase_list = db_obj.get_all_phrases()
    
    
    stored_selectbox = st.selectbox('Stored phrases:', phrase_list)
    default_str = stored_selectbox
    text_input = st.text_input('Enter phrase', default_str)
    submit_button = st.button(label = 'Go')
    
    
    if len(text_input)>0 and submit_button:
        sentiment_obj.send_for_analyze(text_input)
        db_obj.write_row(sentiment_obj.phrase, sentiment_obj.sentiment_response, sentiment_obj.score )  
        sentiment_obj.stream_print()  
        df = db_obj.return_df()
        st.bar_chart(df)

if __name__=="__main__":
    main()