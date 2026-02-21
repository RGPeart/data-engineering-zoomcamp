# AI Coding Agent Instructions

## Project Overview

**data-engineering-zoomcamp** is a structured learning repository for DataTalks Data Engineering Zoomcamp. It's organized into modular sections, each exploring different tools in the modern data stack:

- **`1-docker-terraform/`** – Infrastructure-as-code and containerized data ingestion (active; others are placeholders)
  - `docker-postgres/` – Python data pipeline ingesting NY taxi data into PostgreSQL via Docker Compose
  - `terraform-gcp/` – Terraform configuration for GCP resources (Storage Bucket, BigQuery, etc.)
- **`2-airflow/`, `3-bigquery/`, `4-dbt/`, `5-spark/`** – Future modules (currently empty)

**Key architectural pattern:** Separation of infrastructure (Terraform) from application code (Python scripts). This reflects real-world data engineering where IaC and data pipelines are distinct concerns.

---

## Critical Conventions & Patterns

### 1. **Dependency Management: UV + Locked Dependencies**

This project uses **UV** (fast Python package manager) with **locked dependencies** for reproducibility.

**Files:**
- `pyproject.toml` – Declares runtime and dev dependencies (uv PEP 735 format with `[dependency-groups]`)
- `uv.lock` – Pinned versions for reproducible builds; treat as source control artifact
- `.python-version` – Specifies Python version (currently 3.13)

**Workflow:**
```bash
# Add a new package: update pyproject.toml, then sync
uv add pandas>=2.0
uv sync

# Install without updating lock file (CI/reproducible builds)
uv sync --locked

# Development tools installed separately in dev group
# See pyproject.toml [dependency-groups] dev section
```

**Avoid:** Checking in `uv.lock` changes without updating `pyproject.toml` first. The lock file is auto-generated.

### 2. **Docker & Multi-Stage Builds**

The Dockerfile uses **multi-stage patterns** for efficiency:
- Copies `uv` binary from the official `ghcr.io/astral-sh/uv` image
- Installs dependencies using `uv sync --locked` before copying application code
- Sets `ENV PATH="/app/.venv/bin:$PATH"` so the virtual environment is on the path automatically

**Pattern from `docker-postgres/Dockerfile`:**
```dockerfile
# Copy dependencies first (layer cache optimization)
COPY "pyproject.toml" "uv.lock" ".python-version" ./
RUN uv sync --locked

# Copy application last (changes frequently, no cache invalidation for deps)
COPY ingest_data.py .
```

**Key principle:** Order COPY statements to maximize layer caching; dependencies before code.

### 3. **Python Scripts & Click CLI Framework**

Data ingestion scripts use **Click** for CLI parameter handling instead of hardcoded values or argparse.

**Pattern from `ingest_data.py`:**
```python
@click.command()
@click.option('--pg-user', default='root', help='PostgreSQL user')
@click.option('--pg-pass', default='root', help='PostgreSQL password')
def run(pg_user, pg_pass, ...):
    # Script logic
```

**Why:** Makes scripts composable, testable, and runnable from Docker with environment-specific parameters.

### 4. **Data Type Declarations**

Python data pipelines explicitly define column types using Pandas dtype dicts and `parse_dates`:

```python
dtype = {
    "VendorID": "Int64",
    "trip_distance": "float64",
}
parse_dates = ["tpep_pickup_datetime"]
```

**Why:** Prevents silent type coercions, ensures consistency across runs, and aligns with database schema definitions.

### 5. **Infrastructure: Terraform & GCP**

**File:** `1-docker-terraform/terraform-gcp/main.tf`

**Key pattern:**
- Provider pinned to specific version (e.g., `google 7.16.0`)
- Resources use descriptive names with hyphens (e.g., `google_storage_bucket.demo-bucket`)
- Lifecycle rules and force_destroy flags documented inline

**Important:** Credentials stored in `keys/my-creds.json` are **gitignored** (never committed). Use Terraform variable files or GCP service account environment variables instead.

### 6. **Git Workflow: terraform-dev Branch**

The repository has a `terraform-dev` branch for infrastructure changes separate from `main`.

**Recommended workflow:**
- Feature branches off `terraform-dev` for Terraform/infrastructure changes
- Keep `main` for stable application code only
- Merge `terraform-dev` to `main` only after testing infrastructure changes

**Security:** Ensure sensitive files (`keys/`, `*.tfstate`, `*.tfvars`) are never pushed. The `.gitignore` is configured correctly; verify before committing.

---

## Key Files & Their Roles

| File | Purpose |
|------|---------|
| `1-docker-terraform/docker-postgres/ingest_data.py` | Main data ingestion pipeline; transforms NY taxi CSV → PostgreSQL |
| `1-docker-terraform/docker-postgres/pyproject.toml` | Dependency declarations (pandas, psycopg2, sqlalchemy, etc.) |
| `1-docker-terraform/docker-postgres/Dockerfile` | Container image for pipeline; uses UV for reproducible builds |
| `1-docker-terraform/docker-postgres/docker-compose.yaml` | Local PostgreSQL + pgAdmin setup for development |
| `1-docker-terraform/terraform-gcp/main.tf` | GCP infrastructure (Storage Bucket, BigQuery, etc.) |
| `.gitignore` | Excludes credentials, tfstate files, Python cache, etc. |

---

## Common Tasks & Commands

### Running the Data Pipeline Locally

```bash
# Start PostgreSQL and pgAdmin via Docker Compose
cd 1-docker-terraform/docker-postgres
docker-compose up -d

# Run the ingestion script (assumes data source URL is hardcoded or env var)
python ingest_data.py --pg-user root --pg-pass root --pg-host localhost --pg-port 5432

# Run via Docker
docker build -t de-pipeline .
docker run -e PG_HOST=host.docker.internal de-pipeline --pg-user root --pg-pass root
```

### Managing Dependencies

```bash
# Add a new package
uv add requests

# Add dev-only package
uv add --group dev ipython

# Update lock file
uv lock

# Sync to local environment
uv sync
```

### Working with Terraform

```bash
cd 1-docker-terraform/terraform-gcp

# Initialize Terraform (download provider)
terraform init

# Plan changes
terraform plan -out=tfplan

# Apply infrastructure changes
terraform apply tfplan

# Destroy infrastructure (careful!)
terraform destroy
```

---

## Anti-Patterns to Avoid

1. **Hardcoded credentials or secrets in code** – Use Click options, environment variables, or secret management
2. **Committing `uv.lock` without updating `pyproject.toml`** – Keep these in sync
3. **Committing `*.tfstate` or `keys/` files** – Both are in `.gitignore` for a reason
4. **Skipping Dockerfile layer optimization** – Always COPY dependencies before application code
5. **Inconsistent data types in pandas → database** – Use explicit dtype dicts and schema validation
6. **Running Terraform apply without planning first** – Use `terraform plan` to review changes

---

## Integration Points & Dependencies

- **PostgreSQL 18** – Data store (via Docker Compose)
- **pgAdmin 4** – SQL IDE for development (on localhost:5050)
- **GCP** – Terraform provisions Storage Bucket, BigQuery datasets, etc.
- **pandas, SQLAlchemy, psycopg2** – Data pipeline libraries
- **Click** – CLI framework for parameter handling
- **Terraform 1.x** – Infrastructure-as-code with Google provider 7.16.0

---

## Guidance for New Modules

When expanding to `2-airflow/`, `3-bigquery/`, etc.:

1. Follow the same dependency-management pattern (UV + `pyproject.toml` + `uv.lock`)
2. Keep infrastructure (Terraform) separate from application logic
3. Use Click for Python scripts requiring CLI parameters
4. Document data type assumptions early
5. Use git branches to isolate infrastructure and application changes
6. Ensure all credentials and secrets go into `.gitignore`

