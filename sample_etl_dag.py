from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
}

def extract():
    print("✅ Extracting data")

def transform():
    print("⚠️ Simulating failure in transform step")
    raise Exception("Simulated failure for demo purposes")

def load():
    print("✅ Loading data")

with DAG(
    dag_id='demo_etl_pipeline',
    description='Demo ETL pipeline with failure for monitoring',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['demo'],
) as dag:

    task1 = PythonOperator(task_id='extract', python_callable=extract)
    task2 = PythonOperator(task_id='transform', python_callable=transform)
    task3 = PythonOperator(task_id='load', python_callable=load)

    task1 >> task2 >> task3
