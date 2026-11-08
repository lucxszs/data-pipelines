with ptax as (

    select * from {{ ref('ptax') }}

)

select
    data_cotacao
    , compra
    , venda
    , venda - compra as spread
    , round(100 * (venda / lag(venda) over (order by data_cotacao) - 1), 4) as variacao_venda_pct
from ptax
