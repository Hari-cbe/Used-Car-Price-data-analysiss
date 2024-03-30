from airflow.decorators import dag, task
import pendulum
import os
import logging 

from airflow.operators.python import PythonOperator

@dag(
    dag_id = "test_airflow",
    description= "This is a dag to test the aiflow working",
    start_date = pendulum.datetime(2024,3,13),
    schedule_interval= '@daily',
    catchup= False  
)
def test_airflow():

    @task()
    def check():

        logging.info(os.listdir(os.getcwd()))
        os.makedirs('./data2')    

    check()

test = test_airflow()

