import time
from collections.abc import Iterator
from datetime import date

import requests

from scripts.cnpjpw.domain import constants
from utils.log_utils import log_warning


class CnpjPwClient:
    def __init__(self):
        self.session = requests.Session()
        self.session.headers["User-Agent"] = constants.USER_AGENT

    def _get(self, path: str, params: dict | None = None) -> dict:
        for attempt in range(1, constants.MAX_RETRIES + 1):
            time.sleep(constants.SECONDS_BETWEEN_REQUESTS)
            resp = self.session.get(
                f"{constants.API_URL}{path}",
                params=params,
                timeout=constants.REQUEST_TIMEOUT_SECONDS,
            )
            if resp.status_code not in (429, 503):
                resp.raise_for_status()
                return resp.json()

            wait = 2 ** attempt
            log_warning(
                "extract",
                "API overloaded, backing off",
                status=resp.status_code,
                attempt=f"{attempt}/{constants.MAX_RETRIES}",
                wait=f"{wait}s",
            )
            time.sleep(wait)
        raise RuntimeError(f"cnpj.pw still overloaded after {constants.MAX_RETRIES} attempts: {path}")

    def count_opened_on(self, day: date) -> int:
        return self._get(f"/count/data/{day:%d-%m-%Y}")["total"]

    def cnpjs_opened_on(self, day: date) -> Iterator[str]:
        cursor = None
        while True:
            params = {"cursor": cursor} if cursor else None
            page = self._get(f"/data/{day:%d-%m-%Y}", params)["resultados_paginacao"]
            if not page:
                return
            for company in page:
                yield company["cnpj"]
            cursor = page[-1]["cnpj"]

    def company(self, cnpj: str) -> dict:
        return self._get(f"/cnpj/{cnpj}")
