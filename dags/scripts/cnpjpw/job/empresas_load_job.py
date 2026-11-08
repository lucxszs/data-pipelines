import json
import os
from datetime import date, timedelta

from domain.conn_id import ConnId
from scripts.cnpjpw.client.cnpjpw_client import CnpjPwClient
from scripts.cnpjpw.domain import constants
from utils.log_utils import log_info, log_success
from utils.postgres_utils import upsert_json


class EmpresasLoadJob:
    CONN_ID = str(ConnId.POSTGRES_DWH)

    def extract(self, ds_nodash: str) -> str:
        client = CnpjPwClient()
        day = self._latest_day_with_data(client)
        opened = list(client.cnpjs_opened_on(day))
        cnpjs = self._evenly_spaced_sample(opened)
        log_info("extract", "Sample selected", day=day, opened=len(opened), sample=len(cnpjs))

        os.makedirs(constants.STAGING_DIR, exist_ok=True)
        path = os.path.join(constants.STAGING_DIR, f"empresas_{ds_nodash}.jsonl")
        with open(path, "w", encoding="utf-8") as f:
            for position, cnpj in enumerate(cnpjs, start=1):
                f.write(json.dumps(client.company(cnpj), ensure_ascii=False) + "\n")
                if position % constants.LOG_EVERY_COMPANIES == 0:
                    log_info("extract", "Fetching companies", progress=f"{position}/{len(cnpjs)}")

        log_success("extract", "Companies saved", rows=len(cnpjs), path=path)
        return path

    @staticmethod
    def _evenly_spaced_sample(cnpjs: list[str]) -> list[str]:
        # The API lists CNPJs in order and the first ones of a day are almost all MEI,
        # so taking the head of the list would skew every aggregate.
        step = max(1, len(cnpjs) // constants.MAX_COMPANIES_PER_RUN)
        return cnpjs[::step][:constants.MAX_COMPANIES_PER_RUN]

    def _latest_day_with_data(self, client: CnpjPwClient) -> date:
        for days_ago in range(constants.LOOKBACK_DAYS):
            day = date.today() - timedelta(days=days_ago)
            if client.count_opened_on(day) > 0:
                return day
        raise ValueError(f"cnpj.pw has no companies in the last {constants.LOOKBACK_DAYS} days.")

    def load_bronze(self, path: str) -> None:
        with open(path, encoding="utf-8") as f:
            rows = [(self._cnpj(json.loads(line)), line) for line in f]

        upsert_json(self.CONN_ID, constants.BRONZE_TABLE, constants.BRONZE_KEY, rows)
        log_success("load_bronze", "Rows upserted", rows=len(rows), table=constants.BRONZE_TABLE)

    @staticmethod
    def _cnpj(company: dict) -> str:
        return f"{company['cnpj_base']}{company['cnpj_ordem']}{company['cnpj_dv']}"


def extract_empresas(**context) -> str:
    return EmpresasLoadJob().extract(context["ds_nodash"])


def load_bronze_empresas(**context) -> None:
    EmpresasLoadJob().load_bronze(context["ti"].xcom_pull(task_ids="extract"))
