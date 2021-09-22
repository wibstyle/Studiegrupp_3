import sqlite3
from contextlib import closing
import pandas as pd

class DatabaseHandlerClass():

    def __init__(self):
        self.db_name="Sentiment.db"
        self.table_name="Reflect_sentiment"
        self._create_table2()
       
    def _query(self, sql):
        with closing(sqlite3.connect(self.db_name)) as con, con, closing(con.cursor()) as cur:
            cur.execute(sql)
            return cur.fetchall()

    def return_df(self)-> pd:
        con = sqlite3.connect(self.db_name)
        df = pd.read_sql_query("SELECT sentimental_score from Reflect_sentiment", con)   
        return df

    # def get_row(self):
    #     #c=self.connection.cursor()
    #     sql="SELECT * FROM Reflect_sentiment"
    #     response=self._query(sql)
    #     print(response)
        
    # def get_all(self):
    #     sql="SELECT * FROM Reflect_sentiment"
    #     response=self._query(sql)
    #     print(response)

    def get_all_phrases(self):
        sql="SELECT user_input FROM Reflect_sentiment"
        response=self._query(sql)
        lst=[str(x)[2:-3] for x in response]            # converting tuple to str 
        return lst
        
    def write_row(self, the_phrase:str, the_answer:str, the_score:int ) -> bool:
        sql=f"INSERT INTO Reflect_sentiment VALUES ('{the_phrase}','{the_answer}',{the_score})" 
        response=self._query(sql)
        return True

    # def isRunning(self)-> bool:
    #     return True

    def drop_table(self):
        sql="DROP TABLE IF EXISTS Reflect_sentiment"
        response=self._query(sql)

    def _create_table2(self):
        sql="CREATE TABLE IF NOT EXISTS Reflect_sentiment(user_input  text,sentimental_label text,sentimental_score   REAL)"
        response=self._query(sql)

    # def _check_if_db_exists(self):
    #     try:
    #         print(f'Checking if {self.db_name} exists or not...')
    #         self.connection = sqlite3.connect(self.db_name, uri=True)
    #         print(f'Database exists. Succesfully connected to {self.db_name}')
    #     except sqlite3.OperationalError as err:
    #         print('Database does not exist')
    #         print(err)
    
    
