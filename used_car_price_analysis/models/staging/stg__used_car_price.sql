with source as (

    select * from {{ source('used_car_analysis_dataset', 'used_car_price') }}

),

renamed as (

    select
        vin as vechicle_id_number,
        year as manufactured_year,
        make,
        model,
        trim as additional_design,
        body as body_type,
        transmission,
        state,
        condition,
        odometer,
        color,
        interior,
        seller ,
        mmr as manheim_market_report,
        sellingprice,
        saledate

    from source

)

select * from renamed
