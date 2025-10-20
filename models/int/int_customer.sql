{{ config(materialized='view') }}

select
    customer_id,
    first_name,
    last_name,
    first_name + ' ' + last_name as full_name,
    email,
    phone,
    signup_date
from {{ ref('stg_customer') }}