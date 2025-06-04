from airflow import DAG
from airflow.operators.dagrun_operator import TriggerDagRunOperator
from datetime import datetime

with DAG(
    dag_id='trigger_demo_etl',
    start_date=datetime(2024, 1, 1),
    schedule_interval='@daily',
    catchup=False,
    tags=['trigger'],
) as dag:

    trigger = TriggerDagRunOperator(
        task_id='trigger_etl_pipeline',
        trigger_dag_id='demo_etl_pipeline',
    )
