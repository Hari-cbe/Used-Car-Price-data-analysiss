from airflow.decorators import dag, task 
import pendulum
import os
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
# from airflow.contrib.operators.file_to_gcs import FileToGoogleCloudStorageOperator

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
        src='/home/hariatde_gmail_com/project-used-cars/Used-Car-Price-data-analysiss/data/raw/test.txt',
        dst='gs://used-car-price-analysis/test.txt',
        bucket='used-car-price-analysis',
        gcp_conn_id='gcp_airflow_conn'
    )

    task1 = upload_file

source_to_gcs()