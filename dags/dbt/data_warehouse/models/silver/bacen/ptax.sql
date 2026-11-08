{{ config(
    materialized='incremental',
    incremental_strategy='delete+insert',
    unique_key='data_cotacao',
    indexes=[{'columns': ['data_cotacao'], 'unique': True}]
) }}

with source as (

    select * from {{ source('bronze', 'bacen_ptax') }}
    {% if is_incremental() %}
        where loaded_at > (select coalesce(max(atual.loaded_at), '1900-01-01') from {{ this }} as atual)
    {% endif %}

)

, cotacoes as (

    select
        loaded_at
        , cast(data_hora_cotacao as timestamp) as data_hora_cotacao
        , cast(payload ->> 'cotacaoCompra' as numeric(10, 4)) as compra
        , cast(payload ->> 'cotacaoVenda' as numeric(10, 4)) as venda
    from source

)

select distinct on (cast(data_hora_cotacao as date))
    loaded_at
    , compra
    , venda
    , cast(data_hora_cotacao as date) as data_cotacao
from cotacoes
order by cast(data_hora_cotacao as date) asc, data_hora_cotacao desc
