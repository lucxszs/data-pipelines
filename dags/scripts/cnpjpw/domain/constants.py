API_URL = "https://api.cnpj.pw"
USER_AGENT = "data-pipelines (study project)"
REQUEST_TIMEOUT_SECONDS = 60

# Free service run by one maintainer, limited to 10 requests per IP per second.
SECONDS_BETWEEN_REQUESTS = 0.25
MAX_RETRIES = 5

# About 21k companies open per day and each detail is one request, so a run takes a sample.
MAX_COMPANIES_PER_RUN = 500
LOG_EVERY_COMPANIES = 100

# The source follows the monthly Receita Federal base, so its latest day is weeks old.
LOOKBACK_DAYS = 90

STAGING_DIR = "/usr/local/airflow/include/staging/cnpjpw"

BRONZE_TABLE = "bronze.cnpjpw_empresas"
BRONZE_KEY = "cnpj"
