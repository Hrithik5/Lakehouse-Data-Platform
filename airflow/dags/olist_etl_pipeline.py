from airflow.sdk import dag, task
from pendulum import datetime

from etl_pipeline import run_pipeline


@dag(
    dag_id="olist_etl_pipeline",
    schedule=None,
    start_date=datetime(2026, 1, 1),
    catchup=False,
    tags=["etl", "pyspark", "olist"],
)
def olist_etl_pipeline():

    @task(task_id="run_etl_pipeline")
    def execute_pipeline():
        run_pipeline()

    execute_pipeline()


dag = olist_etl_pipeline()