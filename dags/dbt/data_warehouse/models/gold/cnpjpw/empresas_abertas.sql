with empresas as (

    select * from {{ ref('empresas') }}

)

, socios as (

    select
        cnpj
        , count(*) as qtd_socios
    from {{ ref('socios') }}
    group by cnpj

)

select
    e.cnpj
    , e.razao_social
    , e.nome_fantasia
    , e.data_abertura
    , e.matriz_filial
    , e.cnae_principal
    , e.descricao_cnae
    , e.natureza_juridica
    , e.porte
    , e.capital_social
    , e.situacao_cadastral
    , e.uf
    , e.municipio
    , coalesce(e.is_mei, false) as is_mei
    , coalesce(e.is_simples, false) as is_simples
    , coalesce(s.qtd_socios, 0) as qtd_socios
from empresas as e
left join socios as s
    on e.cnpj = s.cnpj
