{{config(
    partition_by={
        "field" : "saledate",
        "data_type" : "date",
        "granularity": "month"
    }
)}}

with source as (
    select * from {{ref('stg__used_car_price')}} where odometer is not null
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
    CASE 
      when color = '—' then null
      else color
    END color,
    CASE 
        when interior = '—' then null 
        else interior
    END as interior,
    seller ,
    manheim_market_report,
    sellingprice,
    extract(date from saledate) as saledate
from 
    source 