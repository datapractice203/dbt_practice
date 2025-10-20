{{ config(materialized='view') }}

select
    location_id,
    location_name,
    city,
    state,
    country
from {{ ref('stg_location') }}
