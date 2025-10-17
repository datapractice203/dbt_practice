-- models/dev/dev_product.sql
{{ config() }}

select
    product_id::integer as product_id,
    product_name as product_name,
    category as category,
    price::numeric as price
from {{ ref('product') }}
