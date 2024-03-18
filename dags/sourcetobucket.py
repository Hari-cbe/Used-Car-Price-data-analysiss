from airflow.decorators import dag, task 
import pendulum
import os
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor


BUCKET = 'used-car-price-analysis'
GCP_CONN_ID = 'gcp_airflow_conn'

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

    @task()
    def confirm_file():
        return "The File is present"

    
    task1 = upload_file 
    task2 = check_file
    task3 = confirm_file() 

    task1 >> task2 >> task3

source_to_gcs()