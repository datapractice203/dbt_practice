{{ config(materialized='view') }}

select
    rental_id,
    customer_id,
    product_id,
    location_id,
    quantity,
    rental_date,
    return_date
from {{ ref('stg_rental') }}