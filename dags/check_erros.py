from airflow.decorators import dag, task 
import pendulum
import os
import requests
import pandas as pd

# Opearatos and provides for gcp 
from airflow.operators.bash import BashOperator
from airflow.exceptions import AirflowException
from airflow.operators.python import PythonOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
# from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator,IfExistAction


BUCKET = "used-car-price-analysis"
GCP_CONN_ID = "gcp_airflow_conn"
DATASET_NAME = "used_car_analysis_dataset"
CAR_PRICE_TABLE_NAME = "used_car_price"
STATE_ABB_TABLE_NAME = "state_abbrevation"


@dag(
    dag_id = "check_errors",
    description = "This is dag to move source data to gcs ",
    start_date=pendulum.datetime(2024,3,23),
    schedule_interval='@daily',
    catchup=False
)

def check_errors():
        
    def check_values():
        check_value = BigQueryCheckOperator(
            task_id = "check_for_state_abb_table",
            sql = f'SELECT COUNT(*) FROM {DATASET_NAME}.{CAR_PRICE_TABLE_NAME} LIMIT 1',
            gcp_conn_id=GCP_CONN_ID
        )

        try:
        # Execute the task
            result = check_value.execute(context={})
            if result:
                return "pass"
            else:
                return "Kholi"
        except Exception as e:
        # Log the exception if something goes wrong
            print(f"Error occurred: {str(e)}")
            return "Kholi"
        

    check_values_result = PythonOperator(
        task_id = "check_value_for",
        python_callable=check_values
    )

    check_values_result


check_errors()