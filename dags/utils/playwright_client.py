from playwright.sync_api import sync_playwright


class PlaywrightClient:
    """Headless Chromium that runs inside a container and passes basic WAF checks."""

    USER_AGENT = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/124.0.0.0 Safari/537.36"
    )
    LAUNCH_ARGS = [
        "--disable-blink-features=AutomationControlled",
        "--no-sandbox",
        "--disable-dev-shm-usage",
    ]
    TIMEOUT_MS = 60_000

    def __enter__(self) -> "PlaywrightClient":
        self._playwright = sync_playwright().start()
        self._browser = self._playwright.chromium.launch(headless=True, args=self.LAUNCH_ARGS)
        context = self._browser.new_context(
            accept_downloads=True,
            user_agent=self.USER_AGENT,
            locale="pt-BR",
        )
        context.set_default_timeout(self.TIMEOUT_MS)
        self.page = context.new_page()
        return self

    def __exit__(self, exc_type, exc_val, exc_tb) -> None:
        self._browser.close()
        self._playwright.stop()
