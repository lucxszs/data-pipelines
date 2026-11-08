import requests
from airflow.sdk import Variable

from utils.log_utils import log_info, log_success, log_warning

_API_URL = "https://api.telegram.org/bot{token}/sendMessage"


def send_telegram(text: str) -> None:
    """Send a message using the optional `telegram` Variable; without it, do nothing."""
    config = Variable.get("telegram", default=None, deserialize_json=True) or {}
    token = config.get("bot_token")
    chat_id = config.get("chat_id")
    if not token or not chat_id:
        log_info("telegram", "Not configured, skipping")
        return

    try:
        resp = requests.post(
            _API_URL.format(token=token),
            json={"chat_id": chat_id, "text": text},
            timeout=10,
        )
        resp.raise_for_status()
        log_success("telegram", "Message sent")
    except requests.RequestException as e:
        # A notification must never fail the task. The message is left out because
        # it may contain the URL, and the URL contains the bot token.
        log_warning("telegram", "Failed to send message", error=type(e).__name__)
