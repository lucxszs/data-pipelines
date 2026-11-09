from airflow.sdk import DAG
from cosmos.operators import DbtDocsOperator

from domain.dbt_config import DBT_EXECUTABLE, DBT_PROJECT_PATH, profile_config
from domain.defaults import DEFAULT_ARGS
from utils.dbt_docs_utils import publish_dbt_docs

SUMMARY = "Gera a documentação e a linhagem dos modelos dbt e publica no menu Browse do Airflow."

with DAG(
    dag_id="dbt_generate_docs",
    description=SUMMARY,
    doc_md=SUMMARY,
    default_args=DEFAULT_ARGS,
    schedule="30 23 * * *",
    catchup=False,
    max_active_runs=1,
    tags=["dbt", "maintenance"],
) as dag:

    generate_docs = DbtDocsOperator(
        task_id="generate_docs",
        project_dir=str(DBT_PROJECT_PATH),
        profile_config=profile_config,
        dbt_executable_path=DBT_EXECUTABLE,
        callback=publish_dbt_docs,
    )
