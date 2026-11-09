from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG
from cosmos import DbtTaskGroup

from domain.dbt_config import execution_config, profile_config, project_config, render_config_for
from domain.defaults import DEFAULT_ARGS
from scripts.cnpjpw.job.empresas_load_job import extract_empresas, load_bronze_empresas

SUMMARY = (
    "Carrega uma amostra de empresas abertas recentemente da API cnpj.pw e gera "
    "as tabelas de empresas e de aberturas por atividade."
)

with DAG(
    dag_id="cnpjpw_load_empresas",
    description=SUMMARY,
    doc_md=SUMMARY,
    default_args=DEFAULT_ARGS,
    schedule="0 8 * * *",
    catchup=False,
    tags=["cnpjpw", "api", "dbt"],
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_empresas,
    )

    load_bronze = PythonOperator(
        task_id="load_bronze",
        python_callable=load_bronze_empresas,
    )

    transform = DbtTaskGroup(
        group_id="dbt_transform",
        project_config=project_config,
        profile_config=profile_config,
        execution_config=execution_config,
        render_config=render_config_for("cnpjpw"),
    )

    extract >> load_bronze >> transform
