{{ config(materialized='view') }}

select
    customer_id::integer as customer_id,
    first_name as first_name,
    last_name as last_name,
    email as email,
    phone as phone,
    try_to_date(signup_date) as signup_date
from {{ ref('customer') }}