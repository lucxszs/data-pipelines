from domain.conn_id import ConnId
from scripts.gov.client.pep_scraper import PepScraper
from scripts.gov.domain import constants
from utils.log_utils import log_success
from utils.postgres_utils import copy_csv, count_rows, execute_query


class PepLoadJob:
    CONN_ID = str(ConnId.POSTGRES_DWH)

    def extract(self) -> str:
        path = PepScraper().download_csv()
        log_success("extract", "File downloaded", path=path)
        return path

    def load_bronze(self, path: str) -> None:
        columns = ", ".join(f"{c} TEXT" for c in constants.BRONZE_COLUMNS)
        execute_query(self.CONN_ID, f"CREATE SCHEMA IF NOT EXISTS {constants.BRONZE_SCHEMA}")
        execute_query(self.CONN_ID, f"CREATE TABLE IF NOT EXISTS {constants.BRONZE_TABLE} ({columns})")
        execute_query(self.CONN_ID, f"TRUNCATE {constants.BRONZE_TABLE}")
        copy_csv(
            self.CONN_ID,
            constants.BRONZE_TABLE,
            path,
            delimiter=constants.CSV_DELIMITER,
            encoding=constants.CSV_ENCODING,
        )
        rows = count_rows(self.CONN_ID, constants.BRONZE_TABLE)
        log_success("load_bronze", "Table reloaded", rows=rows, table=constants.BRONZE_TABLE)


def extract_pep(**context) -> str:
    return PepLoadJob().extract()


def load_bronze_pep(**context) -> None:
    PepLoadJob().load_bronze(context["ti"].xcom_pull(task_ids="extract"))
