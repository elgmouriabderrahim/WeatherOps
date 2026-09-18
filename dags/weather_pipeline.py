from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime, timedelta

default_args = {
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
}

with DAG(
    dag_id="weatherops_pipeline",
    start_date=datetime(2026, 9, 18),
    schedule="@daily",
    catchup=False,
    default_args=default_args,
) as dag:

    extract = BashOperator(
        task_id="extract",
        bash_command="python extraction/extract.py",
    )

    silver = BashOperator(
        task_id="silver_transformation",
        bash_command="python transformation/clean_cities.py",
    )

    gold = BashOperator(
        task_id="gold_feature_engineering",
        bash_command="python transformation/feature_engineering.py",
    )

    load = BashOperator(
        task_id="load_postgresql",
        bash_command="python load/load_postgres.py",
    )

    extract >> silver >> gold >> load