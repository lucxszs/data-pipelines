from airflow.providers.standard.operators.bash import BashOperator
from airflow.sdk import DAG

from domain.defaults import DEFAULT_ARGS

RETENTION_DAYS = 3
SUMMARY = f"Apaga do banco de metadados do Airflow os XComs com mais de {RETENTION_DAYS} dias."

with DAG(
    dag_id="airflow_clean_xcoms",
    description=SUMMARY,
    doc_md=SUMMARY,
    default_args=DEFAULT_ARGS,
    schedule="0 23 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["airflow", "maintenance"],
) as dag:

    clean_xcoms = BashOperator(
        task_id="clean_xcoms",
        bash_command=(
            "airflow db clean --tables xcom --skip-archive --yes "
            f"--clean-before-timestamp \"$(date -u -d '{RETENTION_DAYS} days ago' +%F)\""
        ),
    )
