import requests
import streamlit as st

class ML_ModelClass():
    
    def __init__(self):
        api_url = f"http://127.0.0.1:8000/sentiment_analysis/"
        self.start_url=f"http://127.0.0.1:8000/start/"
        self.phrase_url=api_url
        self.is_running=""

    # def start_sentiment(self)->int:                     # return status_code
    #     r = requests.get(url = self.start_url)
    #     self.is_running=True
    #     return r

    def send_for_analyze(self, message)-> int:          #hopefully returns 200 and not 4**,5**
        print(message)
        the_response = requests.post( self.phrase_url, json={"context": message } )
        self.response = the_response.json() 
        self.score = self.response['score']
        self.sentiment_response = self.response['sentiment_label']
        self.phrase = message
        
        return the_response.status_code

    def print_answer(self):
        for item_key, item_value in self.response.items():
            print(item_key, item_value)

    def streamlit_print(self):
        for item_key, item_value in self.response.items():
            st.write(item_key, item_value)

    def stream_print(self):
         st.write(self.phrase)
         st.write(self.sentiment_response)
         st.write(self.score)  

    def isRunning(self)-> bool:
        try:
            r = requests.post(self.start_url,json={"name": "sentiment_analysis"})
            r.raise_for_status()  # Raises a HTTPError if the status is 4xx, 5xxx
        except (requests.exceptions.ConnectionError, requests.exceptions.Timeout):
            print ("ML-model server is not running")
            return False
        except requests.exceptions.HTTPError:
            print ("4xx, 5xx")
            return False
        else:
            print ("All good!")  # Proceed to do stuff with `r`
            return True

    def hello_world(self):
        return " hello world hello world hello world"


    def start_analyse_model(self):
        r = requests.post(self.start_url,json={"name": "sentiment_analysis"})
        print (r)
    
    def analyse_model_check(self):
       the_response = requests.post( self.phrase_url, json={"context": "I am a banana"} )
       if the_response.status_code!=200:
           self.start_analyse_model()