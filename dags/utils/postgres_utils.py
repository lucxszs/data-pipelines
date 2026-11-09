from datetime import UTC, datetime

from airflow.providers.postgres.hooks.postgres import PostgresHook


def execute_query(conn_id: str, sql: str) -> None:
    PostgresHook(postgres_conn_id=conn_id).run(sql)


def count_rows(conn_id: str, table: str) -> int:
    return PostgresHook(postgres_conn_id=conn_id).get_first(f"SELECT count(*) FROM {table}")[0]


def upsert_json(conn_id: str, table: str, key_column: str, rows: list[tuple[str, str]]) -> None:
    """Upsert (key, raw JSON) rows into a bronze table, creating it when needed.

    `loaded_at` marks every row of the load, so incremental dbt models read only what changed.
    """
    if not rows:
        raise ValueError(f"No rows to load into {table}.")

    schema = table.split(".")[0]
    execute_query(conn_id, f"CREATE SCHEMA IF NOT EXISTS {schema}")
    execute_query(conn_id, f"""
        CREATE TABLE IF NOT EXISTS {table} (
            {key_column} TEXT PRIMARY KEY,
            payload JSONB NOT NULL,
            loaded_at TIMESTAMPTZ NOT NULL
        )
    """)
    loaded_at = datetime.now(UTC)
    PostgresHook(postgres_conn_id=conn_id).insert_rows(
        table=table,
        rows=[(key, payload, loaded_at) for key, payload in rows],
        target_fields=[key_column, "payload", "loaded_at"],
        replace=True,
        replace_index=key_column,
    )


def copy_csv(conn_id: str, table: str, columns: list[str], filepath: str, delimiter: str, encoding: str) -> None:
    """Bulk load a CSV with COPY, streaming raw bytes so Postgres decodes `encoding`.

    The hook returns a psycopg 2 or 3 connection depending on SQLAlchemy, and each
    driver has its own COPY API.
    """
    sql = (
        f"COPY {table} ({', '.join(columns)}) FROM STDIN WITH "
        f"(FORMAT csv, HEADER true, DELIMITER '{delimiter}', ENCODING '{encoding}')"
    )
    conn = PostgresHook(postgres_conn_id=conn_id).get_conn()
    try:
        with conn.cursor() as cur, open(filepath, "rb") as f:
            if hasattr(cur, "copy_expert"):
                cur.copy_expert(sql, f)
            else:
                with cur.copy(sql) as copy:
                    while chunk := f.read(8192):
                        copy.write(chunk)
        conn.commit()
    except Exception:
        conn.rollback()
        raise
    finally:
        conn.close()
