#### WELCOME  to the streamlit app: Here you interact with three different models and get different response based on your chosen model.
Preparation before running the app
To run the app on your computer you need to have a terminal ready with the following installed 
(python, conda, pandas and pip)in the base enviornment.
It is adviseable to create two new enviornments for the purpose of effectively running the app.
The details are given below.
### First time API integration for running the app. Note: The steps below need to be performed just once.
## 1. Create a new conda environment and activate it
Use the commands below:
conda create --name ENV_NAME python=3.9
conda activate ENV_NAME
## 2. Install requirements
Go to the root folder and install requirements from it.
Use command:
pip install -r requirements.txt
## 3. Installation of streamlit:
Create a new enviornment to run the app.
Follow the same commands i.e.
conda create --name ENV2_NAME python=3.9
conda activate ENV2_NAME
Install streamlit:
Use command:
pip install streamlit
The prepration for running the app are done.
### Steps for running the app.
Note:Every time you wan't to run the app you need to start the API endpoints by following the steps below.
## Start the application from the root folder and activate your newly created enviornment for API
When the enviornment is activated:
Type in the command:
python src/main.py
This will print to the terminal when the application is up.
Leave this terminal running while you follow the other steps.
In another terminal activate the enviornment with the streamlit installed. 
Go to the main folder having the app file.
From inside the folder run the command.
streamlit run ......name of the main app file 
ex. streamlit run streamlit app.py
A new window will open in your browser with the app. # Explore and enjoy the app #
