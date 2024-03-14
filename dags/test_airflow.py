from airflow.decorators import dag, task
import pendulum

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
        print("Hello Mom!, Iam there")

    task1 = check()

test = test_airflow()

