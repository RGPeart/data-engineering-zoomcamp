# Data Warehouse and BigQuery

This module does not have any repository changes. Below are my notes from watching all module videos.

## OnLine Analytical Processing (OLAP)  vs. OnLine Transaction Processing (OLTP)

|---------|  **OLTP**    | **OLAP** |
|---------|----------|------|
| **Purpose** | Control and run essential business operations in real time | Plan, solve problems, support decisions, discover hidden insights, etc. |
| **Data Updates** | Short, fast updates initiated by the user | Data periodically refreshed with scheduled, long-running batch jobs |
| **Database Design** | Normalized databases for efficiency | Denormalized databases for analysis |
| **Space Requirements** | Generally small if historical data is archived | Generally large due to aggregating large datasets| 

- **Data Warehouse** (**DW**) is an **_OLAP solution_** meant for **reporting and data analysis**. Unlike data lakes, which follow the ELT model, DWs commonly use the ETL model
- A DW receives data from data sources which is then processed in a **_staging area_** before being ingested to the actual warehouse (a.k.a. **a database**) and arranged as needed. DWs may then feed data to separate Data Marts; smaller database systems which end users may use for different purposes


- **BigQuery** is a **Serverless Data Warehouse** offered on the Google Cloud Platform
   - There are no servers to manage or database software to install
- Software as well as infrastructure including
   - **Scalability** and **High-Availability**
   - Google takes care of the underlying software and infrastructure management for you
- Built-in features like:
   - Machine learning
   - Geospatial analysis
   - Business Intelligence
- BigQuery maximizes flexibility by separating the compute engine that analyzes your data from your storage
   - This allows the user to budget and reduce their costs
- Some alternatives to BigQuery from other cloud providers include AWS Redshift or Azure Synapse Analytics
- BigQuery's pricing model is separated into 2 main components (**Processing** and **Storage**):
   - **Processing**
      - On-Demand Pricing (default): Example: $5 per TB used per month; the first TB of the month is free
      - Flat Rate Pricing: based on the number of pre-requested slots (virtual CPUs)
         - Queries take up slots. If you're running multiple queries and run out of slots, the additional queries must wait until other queries finish in order to free up a slot and run the query waiting in the queue
         - The flat rate provides 100 slots. So you would have to be using over 400 TB of data processing to consider this option (100 slots at about $2,000 per month)
   - **Storage**
      - The data that is stored in the tables, views, and other BigQuery specific objects

## External Tables
-  BigQuery allows you to create <span style="color:yellow">**External Tables**</span> where the data is actually stored in another area outside of BigQuery
   - But the metadata (such as the table schema) is stored within BigQuery and can still be combined with other tables and queried
   - Be aware that BQ cannot determine processing costs of external tables

## Partitioning
- BigQuery tables can be <span style="color:yellow">**partitioned**</span> into multiple smaller tables
   - Partition tables are very useful to improve performance and reduce costs because BQ will not process as much data per query
   - For example, if we often filter queries based on date, we could partition a table based on date so that we only query a specific sub-table based on the date we are interested in
   - It is best to partition tables based on:
      - Time-Unit Columns: DATE or DATETIME data type columns
      - Ingestion Time: the timestamp when BigQuery ingested the data
      - Integer Ranges: based on similar integers or integer ranges
   - Querying a partitioned table is the exact same as a regular table, with the only difference being the amount of data processed will be drastically different

## Clustering
- Table <span style="color:yellow">**Clustering**</span> consists of rearranging a table based on the values of its columns so that the table is ordered according to any criteria
   - Clustering can be done based on one or multiple columns, up to 4 columns at one time
   - The order of the columns in which the clustering is specified is important in order to determine the column priority
   - Clustering can improve performance and lower costs on big datasets for certain types of queries, such as queries that use filter clauses and queries that aggregate data
      - For example, all the similar columns will be clustered together before they are filtered out much more quickly
   - Clustering columns must be **top-level, non-repeated** columns, such as:
      - DATE
      - BOOL
      - NUMERIC
      - STRING
      - TIMESTAMP
      - DATETIME
   - Partitioned tables can also be clustered. The combination of the two can greatly reduce computing

- **Clustering Facts**:
   - Columns you specify are used to colocate related data
   - Order of the column is important
   - The order of the specified columns determines the sort order of the data
   - Clustering Improves:
      - Filtering queries
      - Aggregate queries
   - Tables with data size < 1GB don't show as significant an improvement with partitioning or clustering


# Partitioning and Clustering

## Partitioning vs. Clustering
| **Topic** | **Partitioning** | **Clustering** | 
| ----- | ------------ | ---------- |
| **Cost**  | Cost known upfront. BQ can estimate the amount of data to be processed before running a query | Cost benefit unknown. BQ cannot estimate the reduction in cost before running a query
| **Granularity** | Low granularity. Only a single column can be used to partition the table | High granularity. Multiple criteria can be used to sort the table |
| **Data Movement** | Partitions can be added, deleted, modified, or even moved between storage options | Clusters are "fixed in place" |
| **Use Case** | Benefits when you filter or aggregate on a single column | Benefits from queries that commonly use filters or aggregation against multiple particular columns |
| **Limitations** | Limited to 4000 partitions; cannot be used in columns with larger cardinality | Unlimited amount of clusters; useful when the cardinality of the number of values a column or group of columns is large |

- You may choose clustering over partitioning when:
   - Partitioning results in a small amount of data per partition (approximately less than 1 GB per partition)
   - When partitioning would result in over 4000 partitions
   - Partitioning results in your mutation operations modifying the majority of partitions in the table frequently (for example, every few minutes)

## Automatic Reclustering
- BigQuery handles the automatic reclustering of tables in the background without any additional costs
- As data is added to a clustered table:
   - The newly inserted data can be written into blocks that contain key ranges that overlap with the key ranges in previously written blocks
   - These overlapping keys weaken the sort property of the table. BQ restores this sort property in the background
- For partitioned tabled, clustering is maintained for data within the scope of each partition


## Best Practices
- **Cost Reduction**
   - Avoid `SELECT *` whenever you can
      - Reducing the amount of columns to display will drastically reduce the amount of processed data and lower costs
   - Price your queries before running them
   - Use clustered and/or partitioned tables if possible
   - Use streaming inserts with caution. They can easily increase costs quickly
   - Materialize query results in stages
- **Query Performance**
   - Filter on partitioned columns
   - Denormalize data
   - Use nested or repeated columns. This will help with denormalizing data
   - Use external data sources appropriately
      - Constantly reading data from a bucket or outside source can incur a lot of additional costs and with weaker performance
   - Reduce data before using the JOIN clause
   - Do not treat WITH clauses (Common Table Expressions 'CTEs') as prepared statements (or stored procedures)
   - Avoid oversharding tables (splitting/partitioning the table into too many small tables)
      - This can increase management costs for metadata and schema checking
   - Avoid JavaScript user-defined functions
   - Use approximate aggregation functions rather than complete ones
   - Order statements should be the last part of the query
   - Optimize the join patterns
   - Place the table with the largest number of rows first, followed by the table with the fewest rows, and then place the remaining tables by decreasing data size
      - This is due to how BigQuery works internally. The first table will be distributed evenly and the second table will be broadcasted to all the nodes


# Internals of BigQuery

## BigQuery Architecture
- BigQuery is built on 4 infrastructure technologies:
   - **Dremel**: the **_compute_** part of BQ. This executes the SQL queries
      - Dremel turns SQL queries into execution trees. The leaves of the trees are called slots and the branches are called **_mixers_**
         - The **slots** are in charge of reading data from storage and perform calculations
         - The **mixers** perform aggregations
      - Dremel dynamically apportions slots to queries as needed, while maintaining fairness for concurrent queries from multiple users
   - **Colossus**: Google's global storage system
      - BQ leverages **_columnar storage format_** and compression algorithms to store data
      - Colossus is optimized for reading large amounts of structured data
      - Colossus also handles replication recovery and distributed management
   - **Jupiter**: the network that connects Dremel and Colossus
      - Jupiter is an in-house network technology created by Google which is used for interconnecting datacenters
   - **Borg**: an orchestration solution that handles everything
      - Borg is a precursor to Kubernetes

            


## Column-Oriented vs Record-Oriented Storage
- Traditional methods for tabular data storage are **record-oriented** (a.k.a. **row-oriented**)
   - Data is read sequentially row by row and then the columns are accessed per row
   - An example is a CSV file, where each new line in the file is a record and all info for that specific record is contained within that line
- BigQuery uses a **columnar storage format**
   - Data is stored according to the columns of the table rather than the rows
   - This is beneficial when dealing with massive amounts of data because it allows us to discard right away the columns we're not interested in when performing queries (which reduce the amount of processed data)
- When performing queries, **Dremel** modifies them in order to create an execution tree: parts of the query are assigned to different mixers, which in turn assign even smaller parts to different slots which will access **Colossus** and retrieve the data

        


# Machine Learning in BigQuery
- BigQuery ML is a BQ feature which allows us to create and execute Machine Learning models using standard SQL queries, without additional knowledge of Python nor any other programming languages and without the need to export data into a different system
- BQ ML offers a variety of ML models depending on the use case as per the image below:
        
- EXAMPLE: you can create ML models directly in the BQ terminal:
    ```
    CREATE OR REPLACE MODEL `taxi-rides-ny.nytaxi.tip_model`
    OPTIONS (
    model_type='linear_reg',
    input_label_cols=['tip_amount'],
    DATA_SPLIT_METHOD='AUTO_SPLIT'
    ) AS
    SELECT
    *
    FROM
    `taxi-rides-ny.nytaxi.yellow_tripdata_ml`
    WHERE
    tip_amount IS NOT NULL;
    ```

- The `CREATE MODEL` clause will create the ML model
- The `OPTIONS()` clause contains all the necessary arguments to create the model:
   - **model_type='linear_reg'** => for specifying that we will create a linear regression model
   - **input_label_cols=['tip_amount']** => lets BQ know that our target feature is tip_amount
   - **DATA_SPLIT_METHOD='AUTO_SPLIT'** => is for automatically splitting the dataset into train/test datasets
- The `SELECT` statement indicates which features need to be considered for training the model
- After the query runs successfully, the BQ explorer in the side panel will show all available models with a special icon
   - Selecting the model will open a new tab with additional info such as model details, training graphs, and evaluation metrics.
- Once you create the model, you will want to **EVALUATE** and **PREDICT** with your new model
   - **EVALUATE EXAMPLE**:
       ```
        SELECT
            *
        FROM
        ML.EVALUATE(
            MODEL `taxi-rides-ny.nytaxi.tip_model`, (
            SELECT
                *
            FROM
                `taxi-rides-ny.nytaxi.yellow_tripdata_ml`
            WHERE
                tip_amount IS NOT NULL
            )
        );
       ```
      - This will output similar metrics to those in the model info, but will contain updated values against the provided training set
   - **PREDICT EXAMPLE**:
       ```
       SELECT
          *
       FROM
          ML.PREDICT(
             MODEL `taxi-rides-ny.nytaxi.tip_model`,(
                SELECT
                   *
                FROM
                   `taxi-rides-ny.nytaxi.yellow_tripdata_ml`
                WHERE
                   tip_amount IS NOT NULL
             ), STRUCT(3 as top_k_features)
          );
        ```
       - The SELECT statement within ML.PREDICT provides the records for which we want to make predictions on
- You can also use **ML.EXPLAIN_PREDICT** to return the prediction along with the most important features that were involved in calculating the prediction for each of the records we want predicted


# Deploying Machine Learning Models From BigQuery
1. ML models created in BigQuery can be exported and deployed to Docker containers running TensorFlow Serving
2. You can export the model to a Google Cloud Storage bucket
    ```
    bq --project_id taxi-rides-ny extract -m nytaxi.tip_model gs://taxi_ml_model/tip_model
    ```
3. Then, you download the exported model to a temporary directory
    ```
    mkdir /tmp/model

    gsutil cp -r gs://taxi_ml_model/tip_model /tmp/model
    ```
4. Create a version subdirectory
    ```
    mkdir -p serving_dir/tip_model/1

    cp -r /tmp/model/tip_model/* serving_dir/tip_model/1

    # Optionally you may erase the temporary directoy
    rm -r /tmp/model
    ```
5. Pull the TensorFlow Serving Docker image and run the image, mounting the version subdirectory you created as a volume and provide a value for the MODEL_NAME environment variable
    ```
    # Make sure you don't mess up the spaces!
    docker run \
        -p 8501:8501 \
        --mount type=bind,source=`pwd`/serving_dir/tip_model,target=/models/tip_model \
        -e MODEL_NAME=tip_model \
        -t tensorflow/serving &
    ```
6. While the image is running, run a prediction with curl, providing values for the features used for the predictions
    ```
    curl \
        -d '{"instances": [{"passenger_count":1, "trip_distance":12.2, "PULocationID":"193", "DOLocationID":"264", "payment_type":"2","fare_amount":20.4,"tolls_amount":0.0}]}' \
        -X POST http://localhost:8501/v1/models/tip_model:predict
    ```
