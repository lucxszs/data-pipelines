from airflow.sdk import DAG
from cosmos.operators.local import DbtSourceLocalOperator

from domain.dbt_config import DBT_EXECUTABLE, DBT_PROJECT_PATH, profile_config
from domain.defaults import DEFAULT_ARGS

SUMMARY = "Verifica se as tabelas bronze foram carregadas dentro do prazo e falha quando alguma está atrasada."

with DAG(
    dag_id="dbt_check_freshness",
    description=SUMMARY,
    doc_md=SUMMARY,
    default_args=DEFAULT_ARGS,
    schedule="0 14 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["dbt", "maintenance"],
) as dag:

    # A stale table will not get fresher in two minutes, so a retry would only delay the alert.
    check_freshness = DbtSourceLocalOperator(
        task_id="check_freshness",
        project_dir=str(DBT_PROJECT_PATH),
        profile_config=profile_config,
        dbt_executable_path=DBT_EXECUTABLE,
        retries=0,
    )
