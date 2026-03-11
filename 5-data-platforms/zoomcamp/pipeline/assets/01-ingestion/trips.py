"""@bruin

# TODO: Set the asset name (recommended pattern: schema.asset_name).
# - Convention in this module: use an `ingestion.` schema for raw ingestion tables.
name: ingestion.trips

# TODO: Set the asset type.
# Docs: https://getbruin.com/docs/bruin/assets/python
type: python

# TODO: Pick a Python image version (Bruin runs Python in isolated environments).
# Example: python:3.11
image: python:3.11

# TODO: Set the connection.
connection: duckdb-default

# TODO: Choose materialization (optional, but recommended).
# Bruin feature: Python materialization lets you return a DataFrame (or list[dict]) and Bruin loads it into your destination.
# This is usually the easiest way to build ingestion assets in Bruin.
# Alternative (advanced): you can skip Bruin Python materialization and write a "plain" Python asset that manually writes
# into DuckDB (or another destination) using your own client library and SQL. In that case:
# - you typically omit the `materialization:` block
# - you do NOT need a `materialize()` function; you just run Python code
# Docs: https://getbruin.com/docs/bruin/assets/python#materialization
materialization:
  # TODO: choose `table` or `view` (ingestion generally should be a table)
  type: table
  # TODO: pick a strategy.
  # suggested strategy: append
  strategy: append

# TODO: Define output columns (names + types) for metadata, lineage, and quality checks.
# Tip: mark stable identifiers as `primary_key: true` if you plan to use `merge` later.
# Docs: https://getbruin.com/docs/bruin/assets/columns
#columns:
#  - name: TODO_col1
#    type: TODO_type
#    description: TODO

@bruin"""

# TODO: Add imports needed for your ingestion (e.g., pandas, requests).
# - Put dependencies in the nearest `requirements.txt` (this template has one at the pipeline root).
# Docs: https://getbruin.com/docs/bruin/assets/python
import json 
import os
from datetime import datetime
from typing import List, Tuple

import pandas as pd
from dateutil.relativedelta import relativedelta

def generate_months_to_ingest(start_date: str, end_date: str) -> List[Tuple[int, int]]:
    start = datetime.strptime(start_date, "%Y-%m-%d")
    end = datetime.strptime(end_date, "%Y-%m-%d")

    if start > end:
      # Optional: Handle cases where start date is after end date
      raise ValueError("Start date must be before or equal to the end date.")

    months_to_ingest = []
    current_date = start

    while current_date <= end:
      months_to_ingest.append((current_date.year, current_date.month))
      current_date += relativedelta(months=1)

    return months_to_ingest


def build_parquet_url(taxi_type: str, year: int, month: int) -> str:
    return f"https://d37ci6vzurychx.cloudfront.net/trip-data/{taxi_type}_tripdata_{year:04d}-{month:02d}.parquet"

def fetch_trip_data(taxi_type: str, year: int, month: int) -> pd.DataFrame:
    url = build_parquet_url(taxi_type, year, month)
    print(f"Fetching: {url}")
    return pd.read_parquet(url)

# TODO: Only implement `materialize()` if you are using Bruin Python materialization.
# If you choose the manual-write approach (no `materialization:` block), remove this function and implement ingestion
# as a standard Python script instead.
def materialize() -> pd.DataFrame:
    """
    TODO: Implement ingestion using Bruin runtime context.

    Required Bruin concepts to use here:
    - Built-in date window variables:
      - BRUIN_START_DATE / BRUIN_END_DATE (YYYY-MM-DD)
      - BRUIN_START_DATETIME / BRUIN_END_DATETIME (ISO datetime)
      Docs: https://getbruin.com/docs/bruin/assets/python#environment-variables
    - Pipeline variables:
      - Read JSON from BRUIN_VARS, e.g. `taxi_types`
      Docs: https://getbruin.com/docs/bruin/getting-started/pipeline-variables

    Design TODOs (keep logic minimal, focus on architecture):
    - Use start/end dates + `taxi_types` to generate a list of source endpoints for the run window.
    - Fetch data for each endpoint, parse into DataFrames, and concatenate.
    - Add a column like `extracted_at` for lineage/debugging (timestamp of extraction).
    - Prefer append-only in ingestion; handle duplicates in staging.
    """

    start_date = os.getenv("BRUIN_START_DATE")
    start_datetime = os.getenv("BRUIN_START_DATETIME")
    end_date = os.getenv("BRUIN_END_DATE")
    end_datetime = os.getenv("BRUIN_END_DATETIME")

    vars = json.loads(os.getenv("BRUIN_VARS", "{}"))
    taxi_types = vars.get("taxi_types", ["yellow", "green"])

    months_to_ingest = generate_months_to_ingest(start_date=start_date, end_date=end_date)

    print(f"Months to ingest: {months_to_ingest}")

    final_dataframe = pd.DataFrame()

    for year, month in months_to_ingest:
      for taxi_type in taxi_types:
        data = fetch_trip_data(taxi_type, year, month)
        data["extracted_at"] = datetime.utcnow()
        final_dataframe = pd.concat([final_dataframe, data], ignore_index=True)

    return final_dataframe


