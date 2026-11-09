from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG
from cosmos import DbtTaskGroup

from domain.dbt_config import execution_config, profile_config, project_config, render_config_for
from domain.defaults import DEFAULT_ARGS
from scripts.bacen.job.ptax_load_job import extract_ptax, load_bronze_ptax

SUMMARY = (
    "Carrega a cotação do dólar (PTAX) da API do Banco Central e gera a tabela "
    "de cotação diária, com spread e variação em relação ao dia anterior."
)

with DAG(
    dag_id="bacen_load_ptax",
    description=SUMMARY,
    doc_md=SUMMARY,
    default_args=DEFAULT_ARGS,
    schedule="0 13 * * 1-5",
    catchup=False,
    tags=["bacen", "api", "dbt"],
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_ptax,
    )

    load_bronze = PythonOperator(
        task_id="load_bronze",
        python_callable=load_bronze_ptax,
    )

    transform = DbtTaskGroup(
        group_id="dbt_transform",
        project_config=project_config,
        profile_config=profile_config,
        execution_config=execution_config,
        render_config=render_config_for("bacen"),
    )

    extract >> load_bronze >> transform
