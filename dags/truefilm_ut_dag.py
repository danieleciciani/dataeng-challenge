from datetime import datetime, timedelta

from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator

default_args = {
    'owner': 'daniele_ciciani',
    'start_date': datetime(2020, 11, 18),
    'retries': 5,
	'retry_delay': timedelta(hours=1)
}

dag = DAG('truefile_unit_tests', description='Truefilm unit testing',
    schedule_interval=None,
    default_args = default_args,
    start_date=datetime(2022, 1, 1), catchup=False)

# Airflow test tasks:

start = DummyOperator(
        task_id='start'
    )

columns_test = BashOperator(
        dag=dag, 
        task_id='columns_test',
        bash_command = 'python -m pytest /opt/airflow/dags/tests/tests-truefilm.py -m columns_validator -v --disable-warnings'
  
    )

data_test = BashOperator(
        dag=dag, 
        task_id='data_test',
        bash_command = 'python -m pytest /opt/airflow/dags/tests/tests-truefilm.py -m data_check -v --disable-warnings'
  
    )

start >> [columns_test, data_test]