FROM astrocrpublic.azurecr.io/runtime:3.3-12-python-3.12

# Chromium is installed as root, so it must live in a path the astro user can read.
ENV PLAYWRIGHT_BROWSERS_PATH=/ms-playwright

USER root

RUN echo 'Acquire::Retries "8";' > /etc/apt/apt.conf.d/80-retries && \
    pip install --no-cache-dir playwright==1.60.0 && \
    playwright install --with-deps chromium
USER astro

# dbt gets its own virtualenv so its dependencies never clash with Airflow's.
RUN python -m venv /usr/local/airflow/dbt_venv && \
    /usr/local/airflow/dbt_venv/bin/pip install --no-cache-dir \
        dbt-core==1.11.16 dbt-postgres==1.11.0
