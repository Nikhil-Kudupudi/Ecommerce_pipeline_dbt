
from datetime import timedelta, datetime

from airflow import DAG 
from airflow.providers.standard.operators.bash import BashOperator
# pip install apache-airflow==3.3.2 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.3.2/constraints-3.12.txt"


default_args ={
    "owner": "airflow",
    "retries": 0,
    'email': ['nikhilkudupudi@gmail.com'], 
    "email_on_failure": True,
    "email_on_retry": False,
    "retry_delay": timedelta(minutes=1)
}
with DAG(dag_id="order_status", default_args=default_args, schedule='@hourly', start_date=datetime(2026, 1, 1), catchup=False) as dag:
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command='source "/home/nikhil/gitrepos/Ecommerce_pipeline_dbt/.venv/bin/activate" && cd "/home/nikhil/gitrepos/Ecommerce_pipeline_dbt/dbt_ecommerce" && dbt run '
    )

    check_order_status = BashOperator(
        task_id="check_order_status",
        bash_command='source "/home/nikhil/gitrepos/Ecommerce_pipeline_dbt/.venv/bin/activate" && python  "/home/nikhil/gitrepos/Ecommerce_pipeline_dbt/airflow_project/dags/utils/check_delayed_orders.py" '
    )

    dbt_run >> check_order_status