{{ config(
    materialized='incremental',
    incremental_strategy='delete+insert',
    unique_key='cnpj',
    indexes=[{'columns': ['cnpj'], 'unique': True}]
) }}

with source as (

    select * from {{ source('bronze', 'cnpjpw_empresas') }}
    {% if is_incremental() %}
        where loaded_at > (select coalesce(max(loaded_at), '1900-01-01') from {{ this }})
    {% endif %}

)

select
    cnpj
    , loaded_at
    , payload ->> 'cnpj_base' as cnpj_base
    , payload ->> 'nome_empresarial' as razao_social
    , nullif(trim(payload ->> 'nome_fantasia'), '') as nome_fantasia
    , cast(payload ->> 'data_inicio_atividade' as date) as data_abertura
    , payload ->> 'identificador_descricao' as matriz_filial
    , payload ->> 'cnae_fiscal_principal' as cnae_principal
    , payload ->> 'cnae_fiscal_principal_descricao' as descricao_cnae
    , payload ->> 'natureza_juridica_desc' as natureza_juridica
    , payload ->> 'porte_empresa_descricao' as porte
    , cast(payload ->> 'capital_social' as numeric(18, 2)) as capital_social
    , payload ->> 'situacao_cadastral_descricao' as situacao_cadastral
    , payload ->> 'uf' as uf
    , payload ->> 'municipio' as cod_municipio
    , payload ->> 'municipio_desc' as municipio
    , cast(payload ->> 'opcao_simples' as boolean) as is_simples
    , cast(payload ->> 'opcao_mei' as boolean) as is_mei
    , payload ->> 'ddd1' as ddd_telefone
    , payload ->> 'telefone_1' as telefone
    , nullif(lower(trim(payload ->> 'correio_eletronico')), '') as email
from source
