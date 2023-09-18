from pydantic import FilePath
from sklearn import preprocessing
from src.preprocessing import cleanup
from src.predict import model_linear
from src.data_scraper import *
import pandas as pd
import numpy as np
from fastapi import FastAPI, Body
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.models import DAG
import airflow
import datetime

scraper_dag = DAG(
    dag_id='scraper_dag', 
    start_date=datetime.datetime(2023,9,14),
    schedule="@daily"
    )
scraping_task = PythonOperator(
    task_id='scraping_task',
    python_callable=data_scraper.py,
    dag=scraper_dag
)


app = FastAPI()

# Returns the predicted house value when requested with the correct information.
@app.post("/predict/")
def prediction(predict: dict = Body()):
    # Both the dataset and prediction values are pre-processed together (if necessary).
    df = pd.read_csv('./data/merged_data.csv')
    df = cleanup(df, predict)
    dfpredict = df.tail(1)
    dfpredict = dfpredict.drop('price', axis=1)
    df = df.drop(df.index[-1])
    predictx = model_linear(df, dfpredict)
    predictx = int(predictx)
    return f"The estimated price is: €{predictx}"

# Returns an example dictionary of the format required to get a prediction.
@app.get("/")
def predictmodel():
    predictx = {
    "Zip code": 0, 
    "subtype": "", 
    "bedrooms": 0, 
    "Living area": 0, 
    "landplot": 0, 
    "facades": 0, 
    "condition": "", 
    "province": ""
    }
    return f"Fill in this dictionary structure and send to endpoint '/predict/' to get a prediction: {predictx}"