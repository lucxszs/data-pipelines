import logging

_log = logging.getLogger("airflow.task")

_STEP_WIDTH = 11


def _write(level: int, symbol: str, step: str, message: str, fields: dict) -> None:
    """Write every project log as: ✔ step        │ message │ key=value · key=value"""
    line = f"{symbol} {step:<{_STEP_WIDTH}} │ {message}"
    if fields:
        line += " │ " + " · ".join(f"{key}={value}" for key, value in fields.items())
    _log.log(level, line)


def log_info(step: str, message: str, **fields) -> None:
    _write(logging.INFO, "•", step, message, fields)


def log_success(step: str, message: str, **fields) -> None:
    _write(logging.INFO, "✔", step, message, fields)


def log_warning(step: str, message: str, **fields) -> None:
    _write(logging.WARNING, "⚠", step, message, fields)


def log_error(step: str, message: str, **fields) -> None:
    _write(logging.ERROR, "✖", step, message, fields)
