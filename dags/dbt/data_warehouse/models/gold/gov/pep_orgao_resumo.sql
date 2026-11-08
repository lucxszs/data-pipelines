with pep as (

    select * from {{ ref('pep') }}

)

select
    nome_orgao
    , count(*) as total_vinculos
    , count(distinct cpf) as pessoas_distintas
    , count(*) filter (
        where data_fim_exercicio is null or data_fim_exercicio >= current_date
    ) as vinculos_ativos
from pep
group by nome_orgao
