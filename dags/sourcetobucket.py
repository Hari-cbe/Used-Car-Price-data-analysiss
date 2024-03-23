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


# Change this value for your use 
BUCKET = "used-car-price-analysis"
GCP_CONN_ID = "gcp_airflow_conn"
DATASET_NAME = "used_car_analysis_dataset"
TABLE_NAME = "used_car_price"

@dag(
    dag_id = "source_to_gcs",
    description = "This is dag to move source data to gcs ",
    start_date=pendulum.datetime(2024,3,14),
    schedule_interval='@daily',
    catchup=False
)
def source_to_gcs():

    @task()
    def get_data_from_source():
        car_sales_csv = pd.read_csv("https://github.com/Hari-cbe/Random-resourses/raw/main/Used-car-price-data/car_sales.csv"
                                    ,delimiter=',')
        car_sales_csv.to_csv('./data/car_sales.csv')

        state_abb_data_csv = pd.read_csv("https://raw.githubusercontent.com/Hari-cbe/Random-resourses/main/Used-car-price-data/data_raw_state_abbrivation.csv"
                                        ,delimiter=',')
        state_abb_data_csv.to_csv('./data/state_abb_data.csv')

    upload_file = LocalFilesystemToGCSOperator(
        task_id="upload_file_gcs",
        src='data/car_sales.csv',
        dst='data/raw/car_sales.csv', 
        bucket=BUCKET,
        gcp_conn_id=GCP_CONN_ID
    )

    # check_file = BigQueryCheckOperator(
    #     task_id = "check_table_is_present",
    #     sql = f"SELECT COUNT(*) from {DATASET_NAME}.used_car_price LIMIT 1",
    #     gcp_conn_id=GCP_CONN_ID
    # )

    def run_bigquery_check():
            # Execute the BigQuery check
            check_file = BigQueryCheckOperator(
                task_id="check_table_is_present",
                sql=f"SELECT COUNT(1) from {DATASET_NAME}.{TABLE_NAME} LIMIT 1",
                gcp_conn_id=GCP_CONN_ID
            )
            
            if check_file:
                  return 0
            else:
                  return 1

# Define the PythonOperator to run the function
    get_result_task = PythonOperator(
        task_id="get_check_result",
        python_callable=run_bigquery_check,
    )
    # Branching based on check result (approach 2)
    
    @task.branch
    def choose_task(get_check_result):
          
        if get_check_result == 0:
            return "task1"
        elif get_check_result == 1:
            return "task2"

    

    create_table_BQ = BigQueryCreateEmptyTableOperator(
        task_id = "create_BQ_table",
        dataset_id = DATASET_NAME,
        if_exists=IfExistAction.SKIP,
        table_id = TABLE_NAME,
        gcp_conn_id = GCP_CONN_ID
    )

    insert_data_bigQuery = GCSToBigQueryOperator(
        task_id = "insert_data_into_table",
        bucket = BUCKET,
        source_objects = [f"data/raw/car_sales.csv"],
        destination_project_dataset_table=f"{DATASET_NAME}.{TABLE_NAME}",
        source_format='CSV',
        gcp_conn_id = GCP_CONN_ID
    )

    task1 = get_data_from_source()
    task2 = upload_file 
    # task3 = check_file
    task4 = get_result_task
    task5 = choose_task(task4)
    task3 = create_table_BQ
    task4 = insert_data_bigQuery

    task1 >> task2 >> task4 >> task5

source_to_gcs()