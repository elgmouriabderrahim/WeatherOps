from airflow.sdk import DAG
from airflow.providers.standard.operators.bash import BashOperator
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

    extract_cities = BashOperator(
    task_id="extract_cities",
    bash_command="cd /app && python extraction/extract_cities.py",
    )

    extract_weather = BashOperator(
        task_id="extract_weather",
        bash_command="cd /app && python extraction/extract_weather.py",
    )

    silver = BashOperator(
        task_id="silver_transformation",
        bash_command="cd /app && python transformation/clean_data.py",
    )

    gold = BashOperator(
        task_id="gold_feature_engineering",
        bash_command="cd /app && python transformation/feature_engineering.py",
    )

    load = BashOperator(
        task_id="load_postgresql",
        bash_command="cd /app && python load/load_postgres.py",
    )

    extract_cities >> extract_weather >> silver >> gold >> load