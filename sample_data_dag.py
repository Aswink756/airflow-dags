from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.email import EmailOperator
from datetime import datetime
import pandas as pd
import os

default_args = {
    'owner': 'airflow',
    'retries': 0,
    'email_on_failure': True,
    'email': ['aswink756@gmail.com'],
}

def extract():
    data = {
        'name': ['Alice', 'Bob', 'Charlie'],
        'age': [25, 30, 35],
        'salary': [50000, 60000, 70000]
    }
    df = pd.DataFrame(data)
    os.makedirs('/opt/airflow/output', exist_ok=True)
    df.to_csv('/opt/airflow/output/raw_data.csv', index=False)

def transform():
    df = pd.read_csv('/opt/airflow/output/raw_data.csv')
    df['salary_in_lakhs'] = df['salary'] / 100000
    df.to_csv('/opt/airflow/output/processed_data.csv', index=False)

def prepare_email_body():
    df = pd.read_csv('/opt/airflow/output/processed_data.csv')
    html_table = df.to_html(index=False, border=1, justify='center')
    with open('/opt/airflow/output/email_body.html', 'w') as f:
        f.write(f"""
        <h3>Hello Aswin,</h3>
        <p>Your ETL DAG has completed successfully. Below is the final processed data:</p>
        {html_table}
        <p>Regards,<br>Apache Airflow</p>
        """)

with DAG(
    dag_id='showcase_etl_email_with_table',
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
    default_args=default_args,
    description='ETL DAG that emails HTML table + CSV',
    tags=["email", "etl", "table"],
) as dag:

    task_extract = PythonOperator(
        task_id='extract',
        python_callable=extract
    )

    task_transform = PythonOperator(
        task_id='transform',
        python_callable=transform
    )

    task_prepare_email = PythonOperator(
        task_id='prepare_email_body',
        python_callable=prepare_email_body
    )

    send_email = EmailOperator(
        task_id='send_email',
        to='aswink756@gmail.com',
        subject='ETL Pipeline Output - Table + CSV',
        html_content="{{ task_instance.xcom_pull(task_ids='prepare_email_body') | safe }}",
        files=['/opt/airflow/output/processed_data.csv']
    )

    task_extract >> task_transform >> task_prepare_email >> send_email
