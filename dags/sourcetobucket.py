from airflow.decorators import dag, task 
import pendulum
import os
import requests
import pandas as pd
import logging

# Opearatos and provides for gcp 
from airflow.operators.bash import BashOperator
from airflow.exceptions import AirflowException
from airflow.operators.python import PythonOperator
from airflow.utils.trigger_rule import TriggerRule
from airflow.providers.google.cloud.transfers.local_to_gcs import LocalFilesystemToGCSOperator
# from airflow.providers.google.cloud.sensors.gcs import GCSObjectExistenceSensor
from airflow.providers.google.cloud.operators.bigquery import BigQueryCheckOperator
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.providers.google.cloud.operators.bigquery import BigQueryCreateEmptyTableOperator,IfExistAction


# Change this value for your use 
BUCKET = "used-car-price-analysis"
GCP_CONN_ID = "gcp_airflow_conn"
DATASET_NAME = "used_car_analysis_dataset"
CAR_PRICE_TABLE_NAME = "used_car_price"
STATE_ABB_TABLE_NAME = "state_abbrevation"

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
        state_abb_data_csv.to_csv('./data/state_abb.csv')

    @task()
    def upload_local_files(**kwargs):
        data_folder = "data/"   
        gcs_path = "data/raw"
        
        csv_files = [file for file in os.listdir(data_folder) if file.endswith('.csv')]
        
        print(f"----- {csv_files}-----")

        # Upload each CSV file to GCS
        for csv_file in csv_files:
            local_file_path = os.path.join(data_folder, csv_file)
            gcs_file_path = f"{gcs_path}/{csv_file}"

            upload_task = LocalFilesystemToGCSOperator(
                task_id=f'upload_to_gcs',
                src=local_file_path,
                dst=gcs_file_path,
                bucket=BUCKET,
                gcp_conn_id=GCP_CONN_ID
            )
            
        upload_task.execute(context=None) 

    
    def run_bigquery_check_for_car_price_table():
            # Execute the BigQuery check
            check_bq_car_price = BigQueryCheckOperator(
                task_id="check_for_car_price_table",
                sql=f"SELECT COUNT(*) from {DATASET_NAME}.{CAR_PRICE_TABLE_NAME} LIMIT 1",
                gcp_conn_id=GCP_CONN_ID
            )

            try:
        # Execute the task
                check_bq_car_price
                return "CAR_PRICE_TABLE_is_found"
            except Exception as e:
        # Log the exception if something goes wrong
                logging.error(f"BigQuery check failed: {str(e)}") 
                return "CAR_PRICE_TABLE_not_found"

    get_result_car_price_table = PythonOperator(
        task_id="get_result_car_price_table",
        python_callable=run_bigquery_check_for_car_price_table
    )


    def run_bigquery_check_for_state_abb_table():
         
        check_value = BigQueryCheckOperator(
             task_id = "check_for_state_abb_table",
             sql = f'SELECT COUNT(*) FROM {DATASET_NAME}.{STATE_ABB_TABLE_NAME} LIMIT 1',
             gcp_conn_id=GCP_CONN_ID
        ) 


        try:
            check_value

        # If the check passes (no exception raised)
            return "STATE_ABB_TABLE_is_found"

        except Exception as e:
        # If the check fails
            logging.error(f"BigQuery check failed: {str(e)}") 

            return "STATE_ABB_TABLE_not_found"
            
    get_result_state_abb_table = PythonOperator(
        task_id="get_result_state_abb_table",
        python_callable=run_bigquery_check_for_state_abb_table
    )

    # Branching based on check result (approach 2)
    @task.branch
    def choose_task(**kwargs):
        ti = kwargs['ti']
        car_price_result = ti.xcom_pull(task_ids="get_result_car_price_table")
        state_abb_result = ti.xcom_pull(task_ids="get_result_state_abb_table")

        if car_price_result == "CAR_PRICE_TABLE_is_found" and state_abb_result == "STATE_ABB_TABLE_is_found":
            return "test_branch"
        return ["create_BQ_table_car_price","create_BQ_table_state_abb"]
    

    # Creating the Big Query table 
    create_table_BQ_car_price = BigQueryCreateEmptyTableOperator(
        task_id = "create_BQ_table_car_price",
        dataset_id = DATASET_NAME,
        if_exists=IfExistAction.SKIP,
        table_id = CAR_PRICE_TABLE_NAME,
        gcp_conn_id = GCP_CONN_ID
    )

    create_table_BQ_state_abb = BigQueryCreateEmptyTableOperator(
        task_id = "create_BQ_table_state_abb",
        dataset_id = DATASET_NAME,
        if_exists=IfExistAction.SKIP,
        table_id = STATE_ABB_TABLE_NAME,
        gcp_conn_id = GCP_CONN_ID
    )

    # Inserting into the big Query table
    insert_data_bigQuery_car_price = GCSToBigQueryOperator(
        task_id = "insert_data_bigQuery_car_price",
        bucket = BUCKET,
        source_objects = [f"data/raw/car_sales.csv"],
        destination_project_dataset_table=f"{DATASET_NAME}.{CAR_PRICE_TABLE_NAME}",
        source_format='CSV',
        gcp_conn_id = GCP_CONN_ID,
        trigger_rule=TriggerRule.ONE_SUCCESS
    )
    insert_data_bigQuery_state_abb = GCSToBigQueryOperator(
        task_id = "insert_data_bigQuery_state_abb",
        bucket = BUCKET,
        source_objects = [f"data/raw/state_abb.csv"],
        destination_project_dataset_table=f"{DATASET_NAME}.{STATE_ABB_TABLE_NAME}",
        source_format='CSV',
        gcp_conn_id = GCP_CONN_ID,
        trigger_rule=TriggerRule.ONE_SUCCESS
    )

    test_bash = BashOperator(
        task_id = "test_branch",
        bash_command="echo Branching..."
    )





    # calling operations
    get_data_from_source = get_data_from_source()
    upload_local_files = upload_local_files()


    get_result_car_price_table = get_result_car_price_table
    get_result_state_abb_table = get_result_state_abb_table

    choose_task = choose_task()

    # Creating and inserting BQ data
    create_table_BQ_car_price = create_table_BQ_car_price
    create_table_BQ_state_abb = create_table_BQ_state_abb

    insert_data_bigQuery_car_price = insert_data_bigQuery_car_price
    insert_data_bigQuery_state_abb = insert_data_bigQuery_state_abb


    test_branching = test_bash


    get_data_from_source >> upload_local_files >> get_result_car_price_table >> get_result_state_abb_table  >> choose_task >> [ create_table_BQ_car_price, create_table_BQ_state_abb , test_branching ]
    create_table_BQ_car_price >> insert_data_bigQuery_car_price
    create_table_BQ_state_abb >> insert_data_bigQuery_state_abb


    
source_to_gcs()