#!/usr/bin/env python
# coding: utf-8

# In[1]:


import pandas as pd


# # Setting Data Types for Taxi Data
# The data types in the csv data file isn't specified, which will raise a warning about mismatched data. We can set the data types of the columns so that pandas does not make any assumptions.

# In[7]:


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

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]


# In[8]:


prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
url = f'{prefix}/yellow_tripdata_2021-01.csv.gz'
print(url)


# In[11]:


df = pd.read_csv(
    url,
    dtype=dtype, # Pulled from dtype variable designed above
    parse_dates=parse_dates # Pulled from parse_date variable designed above
)


# In[12]:


df.head(5)


# # Load Data into Postgres

# In[15]:


from sqlalchemy import create_engine
engine = create_engine('postgresql://root:root@localhost:5432/ny_taxi')


# In[16]:


# Run this to see the SQL statement that will be generated to create this table
print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[17]:


# Run this line to create the table called 'yellow_taxi_data' with just the columns without adding any data
#df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[18]:


# Because this file contains over 1 Million rows, it is best that we break this up into multiple iterations
df_iter = pd.read_csv(
    url,
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000
)


# In[20]:


from tqdm.auto import tqdm

table_not_created = False

for df_chunk in tqdm(df_iter):

    if table_not_created:
        # Create table schema (no data)
        df_chunk.head(0).to_sql(
            name="yellow_taxi_data",
            con=engine,
            if_exists="replace"
        )
        table_not_created = False
        print("Table created")

    # Insert chunk
    df_chunk.to_sql(
        name="yellow_taxi_data",
        con=engine,
        if_exists="append"
    )

    print("Inserted:", len(df_chunk))

