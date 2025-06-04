from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=2),
}

with DAG(
    dag_id='auto_pull_dags_from_github',
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval='@hourly',  # or '@daily'
    catchup=False,
    tags=["maintenance"],
) as dag:

    pull_code = BashOperator(
        task_id='git_pull_latest_dags',
        bash_command='cd /opt/airflow/dags && git pull origin main'
    )

