{{ config(materialized='view') }}

select
    rental_id::integer as rental_id,
    customer_id::integer as customer_id,
    product_id::integer as product_id,
    location_id::integer as location_id,
    quantity::integer as quantity,
    try_to_date(rental_date) as rental_date,
    try_to_date(return_date) as return_date
from {{ ref('rental') }}