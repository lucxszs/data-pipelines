PTAX_URL = (
    "https://olinda.bcb.gov.br/olinda/servico/PTAX/versao/v1/odata/"
    "CotacaoDolarPeriodo(dataInicial=@dataInicial,dataFinalCotacao=@dataFinalCotacao)"
    "?@dataInicial='{start}'&@dataFinalCotacao='{end}'&$format=json"
)
REQUEST_TIMEOUT_SECONDS = 30
WINDOW_DAYS = 30

STAGING_DIR = "/usr/local/airflow/include/staging/bacen"

BRONZE_TABLE = "bronze.bacen_ptax"
BRONZE_KEY = "data_hora_cotacao"
