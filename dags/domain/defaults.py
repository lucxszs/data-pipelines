from datetime import datetime, timedelta

from utils.log_utils import log_error
from utils.telegram_utils import send_telegram


def alert_failure(context) -> None:
    dag_id = context["dag"].dag_id
    ti = context["task_instance"]
    log_error("alert", "Task failed", dag=dag_id, task=ti.task_id, logs=ti.log_url)
    send_telegram(
        f"🚨 Airflow task failed\n"
        f"DAG: {dag_id}\n"
        f"Task: {ti.task_id}\n"
        f"Logs: {ti.log_url}"
    )


DEFAULT_ARGS = {
    "owner": "data-engineering",
    "depends_on_past": False,
    "start_date": datetime(2026, 11, 1),
    "retries": 2,
    "retry_delay": timedelta(minutes=2),
    "on_failure_callback": alert_failure,
}
