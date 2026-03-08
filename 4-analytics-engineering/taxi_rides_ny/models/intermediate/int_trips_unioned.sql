-- Union green and yellow taxi data into a single dataset
-- Demonstrates how to combine data from multiple sources with slightly different schemas

with green_trips as (
    select
        CAST(vendorid AS integer) AS vendor_id,
        CAST(ratecodeid AS integer) AS rate_code_id,
        CAST(pulocationid AS integer) AS pickup_location_id,
        CAST(dolocationid AS integer) AS dropoff_location_id,
        lpep_pickup_datetime,
        lpep_dropoff_datetime,
        store_and_fwd_flag,
        passenger_count,
        trip_distance,
        CAST(trip_type AS integer) AS trip_type,
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        CAST(ehail_fee AS integer) AS ehail_fee,
        improvement_surcharge,
        total_amount,
        payment_type,
        'Green' as service_type
    from {{ ref('stg_green_tripdata') }}
),

yellow_trips as (
    select
        vendor_id,
        rate_code_id,
        pickup_location_id,
        dropoff_location_id,
        pickup_datetime,
        dropoff_datetime,
        store_and_fwd_flag,
        passenger_count,
        trip_distance,
        cast(1 as integer) as trip_type,  -- Yellow taxis only do street-hail (code 1)
        fare_amount,
        extra,
        mta_tax,
        tip_amount,
        tolls_amount,
        cast(0 as numeric) as ehail_fee,  -- Yellow taxis don't have ehail_fee
        improvement_surcharge,
        total_amount,
        payment_type,
        'Yellow' as service_type
    from {{ ref('stg_yellow_tripdata') }}
)

select * from green_trips
union all
select * from yellow_trips