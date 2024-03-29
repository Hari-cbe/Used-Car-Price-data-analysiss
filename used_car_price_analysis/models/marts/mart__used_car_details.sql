select 
    make, 
    model, 
    body_type, 
    transmission,
    odometer,
    color,
    interior as interior_color,
    manufactured_year

from {{ref('int__used_car_price')}}
    
    where make is not null and  
          model is not null and 
          body_type is not null and 
          transmission is not null and 
          odometer is not null and 
          color is not null and 
          interior is not null and 
          manufactured_year is not null