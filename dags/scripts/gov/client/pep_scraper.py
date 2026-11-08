import os
import zipfile

from playwright.sync_api import Page
from playwright.sync_api import TimeoutError as PlaywrightTimeoutError

from scripts.gov.domain import constants
from utils.log_utils import log_warning
from utils.playwright_client import PlaywrightClient


class PepScraper:
    """The portal sits behind a CloudFront WAF, so the download needs a real browser."""

    DOWNLOAD_BUTTON = "#btn"
    PAGE_LOAD_ATTEMPTS = 3
    PAGE_LOAD_TIMEOUT_MS = 60_000
    BUTTON_TIMEOUT_MS = 30_000
    DOWNLOAD_TIMEOUT_MS = 180_000

    def _open_download_page(self, page: Page) -> None:
        for attempt in range(1, self.PAGE_LOAD_ATTEMPTS + 1):
            page.goto(
                constants.PEP_PAGE_URL,
                wait_until="domcontentloaded",
                timeout=self.PAGE_LOAD_TIMEOUT_MS,
            )
            try:
                page.wait_for_selector(self.DOWNLOAD_BUTTON, timeout=self.BUTTON_TIMEOUT_MS)
                return
            except PlaywrightTimeoutError:
                log_warning(
                    "extract",
                    "Download button not rendered",
                    attempt=f"{attempt}/{self.PAGE_LOAD_ATTEMPTS}",
                )

        raise RuntimeError(f"WAF challenge not cleared after {self.PAGE_LOAD_ATTEMPTS} attempts.")

    def download_csv(self) -> str:
        os.makedirs(constants.STAGING_DIR, exist_ok=True)

        with PlaywrightClient() as client:
            self._open_download_page(client.page)
            with client.page.expect_download(timeout=self.DOWNLOAD_TIMEOUT_MS) as download_info:
                client.page.click(self.DOWNLOAD_BUTTON)
            zip_path = os.path.join(constants.STAGING_DIR, download_info.value.suggested_filename)
            download_info.value.save_as(zip_path)

        with zipfile.ZipFile(zip_path) as z:
            csv_name = next(n for n in z.namelist() if n.lower().endswith(".csv"))
            z.extract(csv_name, constants.STAGING_DIR)
        return os.path.join(constants.STAGING_DIR, csv_name)
