from airflow import DAG

from datetime import datetime, timedelta
from airflow.operators.python_operator import PythonOperator
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator

from common.utils import donwload_movie_dataset, load_to_postgres
from common.utils import get_imdb_data, get_wiki_data, write_output

# Global vars
DATA_DIR = 'data/'
OUTPUT_DIR = 'output/'
OUT_TABLE_NAME = 'tf_high_profit_movies'
OUTPUT_FULL_NAME = OUTPUT_DIR + 'high_profit_movies.csv' 
URL_INFO = {
    'imdb_info': 'data/movies_metadata.csv',
    'wiki_info': 'https://dumps.wikimedia.org/enwiki/latest/enwiki-latest-abstract.xml.gz'
}

default_args = {
    'owner': 'daniele_ciciani',
    'start_date': datetime(2020, 11, 18),
    'retries': 5,
	'retry_delay': timedelta(hours=1)
}

dag = DAG('truefile_pipeline_orchestrator', description='Dag truefilm pipeline',
    schedule_interval=None,
    default_args = default_args,
    start_date=datetime(2022, 1, 1), catchup=False)

# Airflow Tasks:
download_data = PythonOperator(
        task_id='1_download-data',
        dag=dag,
        python_callable=donwload_movie_dataset,
        op_kwargs={
            'out_dir': DATA_DIR,
            'urls_dict': URL_INFO
        }
    )

high_profit_movies = SparkSubmitOperator(
    dag=dag,
    task_id='2_spark_processing',
    application='/opt/airflow/dags/high_profit_movies_spark.py',
    conn_id='spark_local', 
    packages='com.databricks:spark-xml_2.12:0.15.0',
    driver_memory='16G',
    application_args=["{{ti.xcom_pull(key='imdb_info')}}",\
                     "{{ti.xcom_pull(key='wiki_info')}}",\
                      OUTPUT_FULL_NAME]
    )

load_to_postgres = PythonOperator(
        task_id='3_load_to_postgres',
        python_callable=load_to_postgres,
        op_kwargs = {
            'table_name': OUT_TABLE_NAME,
            'file_path' : OUTPUT_FULL_NAME
        }
    )

download_data >> high_profit_movies >> load_to_postgres