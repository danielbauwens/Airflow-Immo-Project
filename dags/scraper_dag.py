from src.data_scraper import main
from airflow.operators.python_operator import PythonOperator
from airflow.contrib.sensors.file_sensor import FileSensor
from airflow.models import DAG
import airflow
import datetime

scraper_dag = DAG(
    dag_id='scraper_dag', 
    start_date=datetime.datetime(2023,9,14),
    schedule_interval="@daily",
    catchup=False
    )
scraping_task = PythonOperator(
    task_id='scraping_task',
    python_callable=main(),
    dag=scraper_dag
)
sensor = FileSensor(
    task_id='process',
    poke_interval=20,
    timeout=30,
    filepath='../data/scraped_data.csv',
    dag=scraper_dag
)
merge_task= PythonOperator(
    task_id='merge_task',
    python_callable='merge with pandas in seperate file',
    dag=scraper_dag
)

tr_task = PythonOperator(
    task_id='tr_task',
    python_callable='call this files function to start preprocessing, testing+training and prediction stuff',
    dag=scraper_dag
)

#add in streamlit web server to analyze with graphs

scraping_task >> sensor >> merge_task >> tr_task
