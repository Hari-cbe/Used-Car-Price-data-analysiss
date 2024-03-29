with states as (
    select state, state_abbrivation from {{ref('stg__state_abbrivation')}}
),
used_car_price as(
    select 
        vechicle_id_number,
        state,
        make,
        odometer, 
        sellingprice,
        saledate
    from {{ref('int__used_car_price')}}
)
select 
    vechicle_id_number,
    states.state as state,
    make as makers,
    odometer,
    sellingprice, 
    saledate
from 
    used_car_price 
join states on states.state_abbrivation = used_car_price.state
    where make is not null and odometer is not null