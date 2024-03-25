with source as (

    select * from {{ source('used_car_analysis_dataset', 'used_car_price') }}

),

renamed as (

    select
        year as manufactured_year,
        make,
        model,
        trim,
        body,
        transmission,
        vin,
        state,
        condition,
        odometer,
        color,
        interior,
        seller,
        mmr,
        sellingprice,
        saledate

    from source

)

select * from renamed
