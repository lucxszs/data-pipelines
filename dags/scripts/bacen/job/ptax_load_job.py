import json
import os

from domain.conn_id import ConnId
from scripts.bacen.client.ptax_client import BacenPtaxClient
from scripts.bacen.domain import constants
from utils.log_utils import log_success
from utils.postgres_utils import upsert_json


class PtaxLoadJob:
    CONN_ID = str(ConnId.POSTGRES_DWH)

    def extract(self, ds_nodash: str) -> str:
        quotes = BacenPtaxClient().recent_quotes()

        os.makedirs(constants.STAGING_DIR, exist_ok=True)
        path = os.path.join(constants.STAGING_DIR, f"ptax_{ds_nodash}.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for quote in quotes:
                f.write(json.dumps(quote, ensure_ascii=False) + "\n")

        log_success("extract", "Quotes saved", rows=len(quotes), path=path)
        return path

    def load_bronze(self, path: str) -> None:
        with open(path, encoding="utf-8") as f:
            rows = [(json.loads(line)["dataHoraCotacao"], line) for line in f]

        upsert_json(self.CONN_ID, constants.BRONZE_TABLE, constants.BRONZE_KEY, rows)
        log_success("load_bronze", "Rows upserted", rows=len(rows), table=constants.BRONZE_TABLE)


def extract_ptax(**context) -> str:
    return PtaxLoadJob().extract(context["ds_nodash"])


def load_bronze_ptax(**context) -> None:
    PtaxLoadJob().load_bronze(context["ti"].xcom_pull(task_ids="extract"))
