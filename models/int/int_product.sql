{{ config(materialized='view') }}

select
    product_id,
    product_name,
    category,
    price
from {{ ref('stg_product') }}
