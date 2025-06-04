from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

def task(name): print(f"Running {name}")

with DAG(
    dag_id="parallel_tasks_dag",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False
) as dag:

    t1 = PythonOperator(task_id="task_1", python_callable=lambda: task("1"))
    t2 = PythonOperator(task_id="task_2", python_callable=lambda: task("2"))
    t3 = PythonOperator(task_id="task_3", python_callable=lambda: task("3"))

    # t1 and t2 run in parallel after t3
    t3 >> [t1, t2]
