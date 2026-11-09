import os
from pathlib import Path

from cosmos import ExecutionConfig, ProfileConfig, ProjectConfig, RenderConfig
from cosmos.constants import TestIndirectSelection
from cosmos.profiles import PostgresUserPasswordProfileMapping

from domain.conn_id import ConnId

AIRFLOW_HOME = Path(os.getenv("AIRFLOW_HOME", "/usr/local/airflow"))

DBT_PROJECT_PATH = AIRFLOW_HOME / "dags" / "dbt" / "data_warehouse"
DBT_EXECUTABLE = str(AIRFLOW_HOME / "dbt_venv" / "bin" / "dbt")
DBT_DOCS_DIR = AIRFLOW_HOME / "include" / "dbt_docs"

project_config = ProjectConfig(dbt_project_path=DBT_PROJECT_PATH)

profile_config = ProfileConfig(
    profile_name="data_warehouse",
    target_name="dev",
    profile_mapping=PostgresUserPasswordProfileMapping(
        conn_id=str(ConnId.POSTGRES_DWH),
        profile_args={"schema": "public"},
    ),
)

# Cosmos tests one model at a time, so a test that also reads a sibling model could run
# before that sibling exists. CAUTIOUS skips those tests here; CI runs them in `dbt build`.
execution_config = ExecutionConfig(
    dbt_executable_path=DBT_EXECUTABLE,
    test_indirect_selection=TestIndirectSelection.CAUTIOUS,
)


def render_config_for(tag: str) -> RenderConfig:
    """Select the models of a source. Unit tests use static inputs, so they only run in CI."""
    return RenderConfig(select=[f"tag:{tag}"], exclude=["resource_type:unit_test"])
