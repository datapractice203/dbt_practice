{{ config(materialized='view') }}

select
    downtime_id::integer as downtime_id,
    product_id::integer as product_id,
    start_time::timestamp as start_time,
    end_time::timestamp as end_time,
    reason as reason
from {{ ref('downtime') }}
