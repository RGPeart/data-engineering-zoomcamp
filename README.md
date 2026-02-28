# RGPeart - Data Engineering Zoomcamp Tutorial Walkthrough

A comprehensive learning repository documenting my journey through the **DataTalks Data Engineering Zoomcamp**. This repository contains hands-on implementations and exercises across the modern data stack, designed to build practical skills in data engineering.

## Purpose

This repository serves as a structured workspace for mastering data engineering concepts and tools. Each module covers a distinct area of the data engineering landscape, combining theoretical knowledge with practical, production-ready implementations.

## Repository Structure

The repository is organized into modular sections, each addressing a specific learning objective:

| Module | Directory | Focus Area | Status |
|--------|-----------|-----------|--------|
| **Infrastructure & Data Ingestion** | `1-docker-terraform/` | Docker containerization, data pipelines, Infrastructure-as-Code | ✅ Active |
| **Workflow Orchestration** | `2-airflow/` | Apache Airflow, DAGs, task scheduling | 🔄 Upcoming |
| **Data Warehousing** | `3-bigquery/` | Google BigQuery, SQL analytics, data modeling | 🔄 Upcoming |
| **Data Transformation** | `4-dbt/` | dbt, data modeling, testing, documentation | 🔄 Upcoming |
| **Distributed Processing** | `5-spark/` | Apache Spark, batch processing, large-scale data | 🔄 Upcoming |

## Current Module: Docker & Terraform (1-docker-terraform)

### `docker-postgres/`
Implements a containerized data ingestion pipeline that:
- Extracts NY taxi data from public sources
- Transforms and loads the data into PostgreSQL via SQLAlchemy
- Demonstrates best practices for data pipelines (type safety, error handling, parameterization)
- Uses UV for reproducible dependency management
- Includes Docker Compose for local development (PostgreSQL + pgAdmin)

**Key Technologies:** Python, Docker, PostgreSQL, SQLAlchemy, Pandas, Click CLI

### `terraform-gcp/`
Defines Infrastructure-as-Code for cloud resources using Terraform:
- Provisions Google Cloud Storage buckets for data storage
- Sets up BigQuery datasets for analytics
- Demonstrates Terraform best practices (versioning, resource naming, lifecycle rules)
- Maintains separation between infrastructure and application code

**Key Technologies:** Terraform, Google Cloud Platform (GCP), HCL

## Learning Outcomes

Through this repository, I aim to gain expertise in:

- **Data Pipeline Development** – Building robust, scalable data ingestion and transformation workflows
- **Infrastructure-as-Code** – Managing cloud resources programmatically with Terraform
- **Container Orchestration** – Packaging applications and dependencies with Docker for reproducibility
- **Workflow Orchestration** – Scheduling and monitoring complex data pipelines with Airflow
- **Data Warehousing & Analytics** – Designing efficient schemas and querying large datasets
- **Data Transformation & Testing** – Using dbt for modeling, testing, and documenting data transformations
- **Distributed Processing** – Processing large-scale data with Spark

## Key Conventions

This repository follows several important conventions to ensure code quality and consistency:

### Dependency Management
- Uses **UV** (fast Python package manager) with locked dependencies for reproducibility
- Dependencies declared in `pyproject.toml` with pinned versions in `uv.lock`
- Development and runtime dependencies separated via dependency groups

### Infrastructure & Secrets
- Infrastructure changes tracked on `terraform-dev` branch; application code on `main`
- Sensitive files (`keys/`, `*.tfstate`, `*.tfvars`) excluded via `.gitignore`
- Credentials managed through environment variables or service accounts, never hardcoded

### Code Quality
- Python scripts use Click for parameter handling instead of hardcoded values
- Explicit data type declarations (Pandas dtype dicts) for consistency
- Docker multi-stage builds optimized for layer caching

## Getting Started

To work with the current module:

```bash
# Navigate to the active module
cd 1-docker-terraform/docker-postgres

# Set up the development environment
uv sync

# Start local services (PostgreSQL + pgAdmin)
docker-compose up -d

# Run the data ingestion pipeline
python [ingest_data.py](http://_vscodecontentref_/1) --pg-user root --pg-pass root --pg-host localhost --pg-port 5432