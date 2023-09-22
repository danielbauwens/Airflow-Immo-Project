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

def run_streamlit_app():
    os.system('streamlit run ./immo_app.py')


scraper_dag = DAG(
    dag_id='scraper_dag', 
    start_date=datetime(2023,9,14),
    schedule_interval="@daily",
    catchup=False
    )

scraping_task = PythonOperator(
    task_id='scraping_task',
    python_callable=main,
    dag=scraper_dag
)

cleanup = PythonOperator(
    task_id='cleanup_task',
    python_callable=first_cleanup,
    dag=scraper_dag
)

preprocessor = PythonOperator(
    task_id='process_task',
    python_callable=cleaning,
    dag=scraper_dag
)

tr_task = PythonOperator(
    task_id='tr_task',
    python_callable=training,
    dag=scraper_dag
)

streamlit_task = PythonOperator(
    task_id='streamlit_task',
    python_callable=run_streamlit_app,
    dag=scraper_dag
)
scraping_task >> cleanup >> preprocessor >> tr_task >> streamlit_task
