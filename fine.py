import mysql.connector.cursor
import pandas as pd
import mysql.connector
import matplotlib.pyplot as plt
import plotly.express as px

def st_connect():
    try:
        mydb=mysql.connector.connect(
        host="localhost",
        user="root",
        password="",
        database="police")
        return mydb
    except mysql.connector.Error as e:
        st.error(f"connection error {e}")
        return None
    
def fetch_data(query):
    conn=new_connection()
    if conn:
        try:
            cursor=conn.cursor()
            cursor.execute(query)
            data=cursor.fetchall()
            columns=[desc[0] for desc in cursor.description]
            df=pd.DataFrame(data,columns=columns)
            return df
        finally:
            conn.close()
    else:
        return pd.DataFrame()
    


