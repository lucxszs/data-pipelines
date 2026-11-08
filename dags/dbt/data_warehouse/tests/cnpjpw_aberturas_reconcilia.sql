-- Fails when the aggregate no longer adds up to the number of companies.
{{ config(tags=['cnpjpw']) }}

with agregado as (

    select sum(qtd_empresas) as total from {{ ref('aberturas_por_atividade') }}

)

, detalhe as (

    select count(*) as total from {{ ref('empresas_abertas') }}

)

select
    a.total as total_agregado
    , d.total as total_detalhe
from agregado as a
cross join detalhe as d
where a.total <> d.total
