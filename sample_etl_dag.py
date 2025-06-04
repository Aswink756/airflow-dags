from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

# Default arguments for the DAG
default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(seconds=30),
    'email': ['aswin.b@sganlytics.com'],  # Add email address for failure notifications
    'email_on_failure': True,  # Send email on task failure
    'email_on_retry': False,  # Do not send email on retry
}

# Task functions
def extract():
    print("✅ Extracting data")

def transform():
    print("⚠️ Simulating failure in transform step")
    raise Exception("Simulated failure for demo purposes")

def load():
    print("✅ Loading data")

# Define the DAG
with DAG(
    dag_id='demo_etl_pipeline',
    description='Demo ETL pipeline with failure for monitoring',
    default_args=default_args,
    schedule_interval='@daily',
    start_date=datetime(2024, 1, 1),
    catchup=False,
    tags=['demo'],
) as dag:

    # Define tasks
    task1 = PythonOperator(task_id='extract', python_callable=extract)
    task2 = PythonOperator(task_id='transform', python_callable=transform)
    task3 = PythonOperator(task_id='load', python_callable=load)

    # Set task dependencies
    task1 >> task2 >> task3
