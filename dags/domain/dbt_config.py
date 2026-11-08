import os
from pathlib import Path

from cosmos import ExecutionConfig, ProfileConfig, ProjectConfig
from cosmos.constants import TestIndirectSelection
from cosmos.profiles import PostgresUserPasswordProfileMapping

from domain.conn_id import ConnId

AIRFLOW_HOME = Path(os.getenv("AIRFLOW_HOME", "/usr/local/airflow"))

project_config = ProjectConfig(dbt_project_path=AIRFLOW_HOME / "dags" / "dbt" / "data_warehouse")

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
    dbt_executable_path=str(AIRFLOW_HOME / "dbt_venv" / "bin" / "dbt"),
    test_indirect_selection=TestIndirectSelection.CAUTIOUS,
)
