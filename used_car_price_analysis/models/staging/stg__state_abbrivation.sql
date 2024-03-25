with source as (

    select * from {{ source('used_car_analysis_dataset', 'state_abbrevation') }}

),
select
    string_field_1,
    string_field_2
from source
