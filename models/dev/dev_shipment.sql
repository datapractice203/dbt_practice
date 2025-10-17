-- models/dev/dev_shipments.sql
{{ config() }}

select
    shipment_id::integer as shipment_id,
    rental_id::integer as rental_id,
    shipped_date::date as shipped_date,
    delivered_date::date as delivered_date
from {{ ref('shipment') }}
