
from datetime import timedelta, datetime

from airflow import DAG 
from airflow.providers.standard.operators.bash import BashOperator
# pip install apache-airflow==3.3.2 --constraint "https://raw.githubusercontent.com/apache/airflow/constraints-3.3.2/constraints-3.14.txt"


default_args ={
    "owner": "airflow",
    "retries": 0,
    "email_on_failure": True,
    "email_on_retry": False,
    "retry_delay": timedelta(minutes=1)
}
with DAG(dag_id="order_status", default_args=default_args, schedule_interval='@hourly', start_date=datetime.now().date(), catchup=False) as dag:
    dbt_run = BashOperator(
        task_id="dbt_run",
        bash_command=".venv/Scripts/activate && cd D:/gitRepos/ecommerce/dbt_ecommerce  && dbt run "
    )

    check_order_status = BashOperator(
        task_id="check_order_status",
        bash_command=".venv/Scripts/activate && python -m airflow_project.dags.utils.check_delayed_orders "
    )

    dbt_run >> check_order_status