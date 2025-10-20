{{ config(materialized='view') }}

select
    target_id,
    location_id,
    month,
    target_rentals
from {{ ref('stg_rental_target') }}
