from airflow.decorators import dag, task 
import pendulum
import os

# Opearatos and provides for gcp 
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator


# Change this value for your use 
BUCKET = 'used-car-price-analysis'
GCP_CONN_ID = 'gcp_airflow_conn'
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

    upload_file = LocalFilesystemToGCSOperator(
        task_id="upload_file_gcs",
        src='data/car_sales.csv',
        dst='data/raw/car_sales.csv', 
        bucket=BUCKET,
        gcp_conn_id=GCP_CONN_ID
    )

    check_file = GCSObjectExistenceSensor(
        task_id = "check_file",
        bucket = BUCKET,
        object = 'data/raw/car_sales.csv',
        mode='poke',
        timeout = 60 * 3,
        google_cloud_conn_id = GCP_CONN_ID
    )

    create_table_BQ = BigQueryCreateEmptyTableOperator(
        task_id = "create_BQ_table",
        dataset_id = DATASET_NAME,
        table_id = TABLE_NAME,
        gcp_conn_id = GCP_CONN_ID
    )

    insert_data_bigQuery = GCSToBigQueryOperator(
        task_id = "insert_data_into_table",
        bucket = BUCKET,
        source_objects = [f"data/raw/car_sales.csv"],
        destination_project_dataset_table=f"{DATASET_NAME}.{TABLE_NAME}",
        gcp_conn_id = GCP_CONN_ID
    )

    task1 = upload_file 
    task2 = check_file
    task3 = create_table_BQ
    task4 = insert_data_bigQuery

    task1 >> task2 >> task3 >> task4

source_to_gcs()