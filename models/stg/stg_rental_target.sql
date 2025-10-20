{{ config(materialized='view') }}

select
    target_id::integer as target_id,
    location_id::integer as location_id,
    month as month,
    target_rentals::integer as target_rentals
from {{ ref('rental_target') }}
