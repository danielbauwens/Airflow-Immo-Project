from airflow.operators.python import PythonOperator
from airflow.sensors.filesystem import FileSensor
from airflow.models import DAG
from src.data_scraper import *
from src.analysis import first_cleanup
from src.preprocessing import cleaning
from src.predict import training
from datetime import datetime 
import pandas as pd
import os

# Function to run the local streamlit app on 'localhost:8051'
def run_streamlit_app():
    os.system('streamlit run ./immo_app.py')

# Initialization of the DAG, setting a start-date and schedule interval. Also declaring no catchup needed.
scraper_dag = DAG(
    dag_id='scraper_dag', 
    start_date=datetime(2023,9,14),
    schedule_interval="@daily",
    catchup=False
    )
# First task runs the scraping file
scraping_task = PythonOperator(
    task_id='scraping_task',
    python_callable=main,
    dag=scraper_dag
)
# Second task runs a basic cleanup, fillna's as well as adds unified city names + provinces
cleanup = PythonOperator(
    task_id='cleanup_task',
    python_callable=first_cleanup,
    dag=scraper_dag
)
# Third task prepares for training. Get dummies is used on modified zip codes as well as provinces to get higher prediction accuracy.
preprocessor = PythonOperator(
    task_id='process_task',
    python_callable=cleaning,
    dag=scraper_dag
)
# Fourth task trains the data with the test_training model from scikit learn, and stores it in a joblib dump
tr_task = PythonOperator(
    task_id='tr_task',
    python_callable=training,
    dag=scraper_dag
)
# Fifth and final task hosts a local web app which displays the final dataframe.
streamlit_task = PythonOperator(
    task_id='streamlit_task',
    python_callable=run_streamlit_app,
    dag=scraper_dag
)
scraping_task >> cleanup >> preprocessor >> tr_task >> streamlit_task
