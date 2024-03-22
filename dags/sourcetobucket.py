from airflow.decorators import dag, task 
import pendulum
import os
import requests

# Opearatos and provides for gcp 
from airflow.operators.bash import BashOperator
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
# from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
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
        #Want to change this 
        car_price_data = requests.get("https://d37ci6vzurychx.cloudfront.net/trip-data/yellow_tripdata_2024-01.parquet")
        
        if car_price_data.status_code == 200:
        # Save the content of the response to a local CSV file
            with open("./data/sample.csv", "wb") as f:
                f.write(car_price_data.content)
            print("car_price_data.csv file downloaded successfully")
        else:
            print("Failed to download car_sales.csv file. Status code:", car_price_data.status_code)


        state_abb_data = requests.get("https://github.com/Hari-cbe/Random-resourses/blob/main/Used-car-price-data/data_raw_state_abbrivation.csv")
        
        if state_abb_data.status_code == 200:
        # Save the content of the response to a local CSV file
            with open("./data/state_abb_data.csv", "wb") as f:
                f.write(state_abb_data.content)
            print("state_abb_data.csv file downloaded successfully")
        else:
            print("Failed to download CSV file. Status code:", state_abb_data.status_code)

    upload_file = LocalFilesystemToGCSOperator(
        task_id="upload_file_gcs",
        src='data/car_sales.csv',
        dst='data/raw/car_sales.csv', 
        bucket=BUCKET,
        gcp_conn_id=GCP_CONN_ID
    )

    # check_file = GCSObjectExistenceSensor(
    #     task_id = "check_file",
    #     bucket = BUCKET,
    #     object = 'data/raw/car_sales.csv',
    #     mode='poke', # default mode 'poke'
    #     timeout = 60 * 3,
    #     google_cloud_conn_id = GCP_CONN_ID
    # )

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
    task3 = create_table_BQ
    task4 = insert_data_bigQuery

    task1 >> task2 >> task3 >> task4

source_to_gcs()