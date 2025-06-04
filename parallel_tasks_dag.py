from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime, timedelta

def task(name):
    print(f"Running {name}")

# You should avoid using lambda directly — define functions for reliability
def run_task_1():
    task("1")

def run_task_2():
    task("2")

def run_task_3():
    task("3")

default_args = {
    'owner': 'airflow',
    'retries': 1,
    'retry_delay': timedelta(minutes=1),
    'email': ['aswin.b@sganlytics.com'],
    'email_on_failure': True,
    'email_on_retry': False
}

with DAG(
    dag_id="parallel_tasks_dag",
    default_args=default_args,
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    tags=["parallel"],
) as dag:

    t1 = PythonOperator(task_id="task_1", python_callable=run_task_1)
    t2 = PythonOperator(task_id="task_2", python_callable=run_task_2)
    t3 = PythonOperator(task_id="task_3", python_callable=run_task_3)

    # t1 and t2 run in parallel after t3
    t3 >> [t1, t2]
