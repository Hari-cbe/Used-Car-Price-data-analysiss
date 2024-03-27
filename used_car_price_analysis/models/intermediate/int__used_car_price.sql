{{config(
    partition_by={
        "field" : "saledate",
        "data_type" : "date",
        "granularity": "month"
    }
)}}

with source as (
    select * from {{ref('stg__used_car_price')}}
)
select  
    vechicle_id_number,
    manufactured_year,
    make,
    model,
    body_type,
    transmission,
    state,
    condition,
    odometer,
    color,
    interior,
    seller ,
    manheim_market_report,
    sellingprice,
    extract(date from saledate) as saledate
from 
    source 