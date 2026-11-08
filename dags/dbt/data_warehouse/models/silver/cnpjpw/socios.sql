{# delete+insert by cnpj replaces all the partners of a company that changed. #}
{{ config(
    materialized='incremental',
    incremental_strategy='delete+insert',
    unique_key='cnpj',
    indexes=[{'columns': ['cnpj']}]
) }}

with source as (

    select * from {{ source('bronze', 'cnpjpw_empresas') }}
    {% if is_incremental() %}
        where loaded_at > (select coalesce(max(loaded_at), '1900-01-01') from {{ this }})
    {% endif %}

)

select
    s.cnpj
    , s.loaded_at
    , socio ->> 'nome' as nome_socio
    , socio ->> 'cnpj_cpf' as documento_socio
    , cast(socio ->> 'data_entrada_sociedade' as date) as data_entrada_sociedade
from source as s
cross join lateral jsonb_array_elements(
    case
        when jsonb_typeof(s.payload -> 'socios') = 'array' then s.payload -> 'socios'
        else cast('[]' as jsonb)
    end
) as socio
