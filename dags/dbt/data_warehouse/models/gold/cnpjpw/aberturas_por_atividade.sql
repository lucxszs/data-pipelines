with empresas as (

    select * from {{ ref('empresas_abertas') }}

)

select
    data_abertura
    , uf
    , cnae_principal
    , descricao_cnae
    , count(*) as qtd_empresas
    , count(*) filter (where is_mei) as qtd_mei
    , sum(capital_social) as capital_social_total
from empresas
group by data_abertura, uf, cnae_principal, descricao_cnae
