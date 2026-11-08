PEP_PAGE_URL = "https://portaldatransparencia.gov.br/download-de-dados/pep"

STAGING_DIR = "/usr/local/airflow/include/staging/gov"

CSV_DELIMITER = ";"
CSV_ENCODING = "LATIN1"

BRONZE_SCHEMA = "bronze"
BRONZE_TABLE = "bronze.gov_pep"
BRONZE_COLUMNS = [
    "cpf", "nome_pep", "sigla_funcao", "descricao_funcao", "nivel_funcao",
    "nome_orgao", "data_inicio_exercicio", "data_fim_exercicio", "data_fim_carencia",
]
