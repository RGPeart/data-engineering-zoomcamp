#!/usr/bin/env python
# coding: utf-8

import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm

## SET TABLE COLUMN DATA TYPES
dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

## SET THE DATE COLUMNS THAT WILL NEED TO BE PARSED USING parse_dates
parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

def run():
    ## SET PARAMETERS
    year = 2021
    month = 1

    pg_user = 'root'
    pg_pass = 'root'
    pg_host = 'localhost'
    pg_port = 5432
    pg_db = 'ny_taxi'

    chunk_size = 100000

    target_table = 'yellow_taxi_data'

    ## READ DATA
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    url = f'{prefix}/yellow_tripdata_{year}-{month:02d}.csv.gz'

    df = pd.read_csv(
        url,
        dtype=dtype, # Pulled from dtype variable designed above
        parse_dates=parse_dates # Pulled from parse_date variable designed above
    )

    ## LOAD DATA INTO POSTGRES
    engine = create_engine(f'postgresql://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')

    # Because this file contains over 1 Million rows, it is best that we break this up into multiple iterations
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunk_size
    )

    # Run this to see the SQL statement that will be generated to create this table
    print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))

    table_not_created = False

    # Run this line to create the table called 'yellow_taxi_data' with just the columns without adding any data
    #df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')

    for df_chunk in tqdm(df_iter):

        if table_not_created:
            # Create table schema (no data)
            df_chunk.head(0).to_sql(
                name=target_table,
                con=engine,
                if_exists="replace"
            )
            table_not_created = False
            print("Table created")

        # Insert chunk
        df_chunk.to_sql(
            name=target_table,
            con=engine,
            if_exists="append"
        )

        print("Inserted:", len(df_chunk))

if __name__ == '__main__':
    run()