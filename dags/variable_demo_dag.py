from airflow import DAG
from airflow.hooks.base import BaseHook
from airflow.models import Variable
from airflow.operators.python import PythonOperator
from datetime import datetime

def print_var():
    my_var = Variable.get("example-variable")
    print(f'My variable is: {my_var}')


with DAG('example_secrets_dag', start_date=datetime(2022, 1, 1), schedule_interval=None) as dag:

  test_task = PythonOperator(
      task_id='test-task',
      python_callable=print_var
)