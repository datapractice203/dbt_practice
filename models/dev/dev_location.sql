-- models/dev/dev_location.sql
{{ config() }}

select
    location_id::integer as location_id,
    location_name as location_name,
    city as city,
    state as state,
    country as country
from {{ ref('location') }}
