with source as (

    select * from {{ source('bronze', 'gov_pep') }}

)

select distinct
    nullif(trim(cpf), '') as cpf
    , trim(nome_pep) as nome_pep
    , nullif(trim(sigla_funcao), '') as sigla_funcao
    , nullif(trim(descricao_funcao), '') as descricao_funcao
    , nullif(trim(nivel_funcao), '') as nivel_funcao
    , trim(nome_orgao) as nome_orgao
    , to_date(nullif(data_inicio_exercicio, 'Não informada'), 'DD/MM/YYYY') as data_inicio_exercicio
    , to_date(nullif(data_fim_exercicio, 'Não informada'), 'DD/MM/YYYY') as data_fim_exercicio
    , to_date(nullif(data_fim_carencia, 'Não informada'), 'DD/MM/YYYY') as data_fim_carencia
from source
