from datetime import timedelta

from airflow.providers.standard.operators.python import PythonOperator
from airflow.sdk import DAG
from cosmos import DbtTaskGroup, RenderConfig

from domain.dbt_config import execution_config, profile_config, project_config
from domain.defaults import DEFAULT_ARGS
from scripts.gov.job.pep_load_job import extract_pep, load_bronze_pep

with DAG(
    dag_id="gov_load_pep",
    default_args=DEFAULT_ARGS,
    schedule="0 6 2 * *",
    catchup=False,
    tags=["gov", "scraping", "dbt"],
) as dag:

    extract = PythonOperator(
        task_id="extract",
        python_callable=extract_pep,
        execution_timeout=timedelta(minutes=8),
    )

    load_bronze = PythonOperator(
        task_id="load_bronze",
        python_callable=load_bronze_pep,
    )

    transform = DbtTaskGroup(
        group_id="dbt_transform",
        project_config=project_config,
        profile_config=profile_config,
        execution_config=execution_config,
        render_config=RenderConfig(select=["tag:gov"]),
    )

    extract >> load_bronze >> transform
