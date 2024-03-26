with source as (

    select * from {{ source('used_car_analysis_dataset', 'state_abbrevation') }}

)
select state, state_abbrevation from (
    select
        row_number() over() as rn,
        string_field_1 as state,
        string_field_2 as state_abbrevation
    from source
) as b
where rn > 1
