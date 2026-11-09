import shutil
from pathlib import Path

from domain.dbt_config import DBT_DOCS_DIR
from utils.log_utils import log_success

DOCS_FILES = ["index.html", "manifest.json", "catalog.json"]


def publish_dbt_docs(project_dir: str, **_) -> None:
    """Copy the generated docs to a folder the API server can read.

    Cosmos runs dbt in a temporary copy of the project, deleted when the task ends.
    """
    DBT_DOCS_DIR.mkdir(parents=True, exist_ok=True)
    for name in DOCS_FILES:
        shutil.copy(Path(project_dir) / "target" / name, DBT_DOCS_DIR / name)
    log_success("publish", "dbt docs published", path=DBT_DOCS_DIR)
