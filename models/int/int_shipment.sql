{{ config(materialized='view') }}

select
    shipment_id,
    rental_id,
    shipped_date,
    delivered_date
from {{ ref('stg_shipment') }}
