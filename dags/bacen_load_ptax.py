from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG
from cosmos import DbtTaskGroup, RenderConfig

from domain.dbt_config import execution_config, profile_config, project_config
from domain.defaults import DEFAULT_ARGS
from scripts.bacen.job.ptax_load_job import extract_ptax, load_bronze_ptax

with DAG(
    dag_id="bacen_load_ptax",
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
        render_config=RenderConfig(select=["tag:bacen"]),
    )

    extract >> load_bronze >> transform
