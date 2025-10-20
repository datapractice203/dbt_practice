{{ config(materialized='view') }}

select
    downtime_id,
    product_id,
    start_time,
    end_time,
    reason
from {{ ref('stg_downtime') }}
