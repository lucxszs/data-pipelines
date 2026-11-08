from datetime import datetime, timedelta

import requests

from scripts.bacen.domain import constants


class BacenPtaxClient:
    def recent_quotes(self) -> list[dict]:
        end = datetime.today()
        start = end - timedelta(days=constants.WINDOW_DAYS)
        url = constants.PTAX_URL.format(start=f"{start:%m-%d-%Y}", end=f"{end:%m-%d-%Y}")

        resp = requests.get(url, timeout=constants.REQUEST_TIMEOUT_SECONDS)
        resp.raise_for_status()
        return resp.json().get("value", [])
