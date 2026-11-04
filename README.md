# Shop Pipeline — A Reproducible, Validated Data Pipeline

A data pipeline that transforms raw online-shop order data into clean, validated, and analysis-ready outputs.

The project focuses on data quality, reproducibility, validation, data lineage, and reliable data processing.

## Project Overview

The pipeline processes monthly order exports and customer master data through a structured workflow:

**Raw Data → Cleaning → Validation → Splitting → Enrichment → Outputs**

It separates trusted records from problematic records, documents data transformations, and generates business summaries.

## Setup and Run

### 1. Clone the repository

```bash
git clone https://github.com/jasmeetkaurpelia/dm-shop_pipeline-group-07.git
cd dm-shop_pipeline-group-07
```

### 2. Create a virtual environment

```bash
python -m venv .venv
```

Activate it:

**Windows (PowerShell):**
```powershell
.venv\Scripts\Activate.ps1
```

**Linux / macOS:**
```bash
source .venv/bin/activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Run the pipeline

```bash
python pipeline.py
```

Each run appends information to `logs/run_log.txt`. Repeated runs with unchanged input data and configuration should produce consistent results.

## Project Structure

```text
shop_pipeline/
├── README.md
├── requirements.txt
├── pipeline.py
├── rules.py
├── cleaning_log.md
├── lineage.md
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── orders_2026_01.csv
│   │   ├── orders_2026_02.csv
│   │   └── orders_2026_03.csv
│   └── output/
        ├── clean_customers.csv
        ├── fct_orders.csv
        ├── quarantine_orders.csv
        ├── revenue_by_city.csv
        └── revenue_by_category.csv
├── logs/
│   └── run_log.txt
└── extras/
    └── orders_2026_04.csv
```

The `data/raw/` directory contains the original input files. These files are read by the pipeline and are not overwritten.

Generated outputs are stored in `data/output/`, while execution details are recorded in `logs/`.

## Input Data

| File | Contents |
|---|---|
| `orders_2026_01.csv` | January order records |
| `orders_2026_02.csv` | February order records |
| `orders_2026_03.csv` | March order records |
| `customers.csv` | Customer master data |
| `orders_2026_04.csv` | Additional order data supplied in `extras/` |

**Order fields:** `order_id`, `order_date`, `customer_id`, `category`, `quantity`, `unit_price`

**Customer fields:** `customer_id`, `customer_name`, `city`, `country`, `email`, `segment`

## Pipeline Workflow

| Stage | Function | Description |
|---|---|---|
| Load | `load_raw()` | Reads monthly order files and adds `source_file` to preserve data lineage. |
| Clean | `clean_orders()`, `clean_customers()` | Removes exact duplicates, trims text, parses dates, and converts numeric values. |
| Validate | `validate()` | Applies validation rules defined in `rules.py`. Critical validation failures stop processing. |
| Split | `split()` | Separates trusted records from records that require quarantine and applies the known March price correction. |
| Enrich | `enrich_orders()` | Adds customer city information and calculates `line_total`. |
| Output | `output()` | Writes the output datasets and records the run information. |

## Data Quality: Stop or Quarantine?

The pipeline distinguishes between two types of data-quality problems:

- **Stop:** Critical issues that affect the reliability or structure of the dataset, such as duplicate order IDs or invalid identifiers.
- **Quarantine:** Problems affecting individual records, such as missing prices, invalid quantities, missing dates, or unknown customers.

Quarantined records are retained separately rather than silently included in trusted outputs.

## Outputs and Data Dictionary

All generated CSV files are stored in `data/output/`.

### `clean_customers.csv`

Contains all customer records after cleaning and validation.

The original customer input file remains unchanged. The cleaned output includes:

- Trimmed whitespace in text fields.
- Standardised the known country spelling error (`Germny` to `Germany`).
- Replaced the known malformed email with an empty value because the correct address could not be determined.

The output retains the customer columns:

| Column | Description |
|---|---|
| `customer_id` | Unique customer identifier |
| `customer_name` | Customer name |
| `city` | Customer city |
| `country` | Standardised country |
| `email` | Customer email; may be empty |
| `segment` | Customer segment |

### `fct_orders.csv`

Contains trusted order records ready for analysis.

| Column | Description | Unit / Rule |
|---|---|---|
| `order_id` | Order identifier | One capital letter followed by three digits; unique |
| `order_date` | Order date | Parsed datetime |
| `customer_id` | Customer identifier | Must exist in customer data |
| `category` | Product category | Accessories or Electronics |
| `quantity` | Number of items ordered | Greater than 0 |
| `unit_price` | Price per item | EUR, greater than or equal to 0 |
| `source_file` | Original input filename | Used for data lineage |
| `city` | Customer's city | Retrieved from customer master data |
| `line_total` | Revenue for the order line | `quantity × unit_price`, EUR |

### `quarantine_orders.csv`

Contains order records that fail row-level checks and are excluded from the trusted dataset.

It retains the original order fields and source information so that problematic records can be investigated.

### `revenue_by_city.csv`

Aggregates trusted order revenue by customer city.

| Column | Description | Unit |
|---|---|---|
| `city` | Customer's city | Text |
| `line_total` | Total revenue for the city | EUR |

### `revenue_by_category.csv` — New output

Aggregates trusted order revenue by product category.

| Column | Description | Unit |
|---|---|---|
| `category` | Product category | Text |
| `line_total` | Total revenue for the category | EUR |

## Validation Rules

Validation rules are defined in `rules.py` and applied before the pipeline creates its trusted outputs.

### Order validation

- `order_id` must follow the expected identifier format and be unique.
- `customer_id` must not be empty.
- `category` must be either Accessories or Electronics.
- `unit_price` must not be negative.
- `order_date` must not be in the future.
- `source_file` must not be empty.

### Customer validation

- `customer_id` must follow the expected identifier format and be unique.
- `customer_name` must not be empty.
- `email` must follow the expected email format or be empty.
- `country` must be Germany, Austria, or Switzerland.

Critical validation failures stop the pipeline. Individual row-level problems are handled by the quarantine step.

## Data Cleaning and Documentation

The cleaning operations and reasons for each transformation are recorded in `cleaning_log.md`.

The pipeline also preserves source-file information through the `source_file` column, allowing records to be traced back to their original input files.

## Data Lineage

The pipeline's data flow is documented in `lineage.md`.

The lineage diagram shows how raw order and customer files move through loading, cleaning, validation, splitting, enrichment, and output generation.

## Technologies

- Python
- Pandas
- Pandera
- CSV
- Git and GitHub

## Team Members

| Name | Role / Contribution |
|---|---|
| Jasmeet Kaur | Pipeline development: implemented the main Python pipeline, data loading, cleaning, transformations, Pandera validation rules, trusted/quarantine separation, data enrichment, and revenue aggregations. Also worked on project documentation and Git version control. |
| Yash Chinnannavar | Data quality and validation: supported the review of data-quality requirements, validation results, and identification of problematic records. |
| Vivek Sawant, | Data analysis and outputs: supported the review of generated datasets, revenue summaries, and interpretation of output results. |
| Shashank Kenkere Sridhar | Documentation and data lineage: supported the review of the data dictionary, cleaning log, README, and pipeline lineage diagram. |
| Keshav sain | Testing and reproducibility: supported pipeline testing, checking execution logs, reviewing project structure, and verifying the setup and run instructions. |

## Reproducibility

To reproduce the pipeline:

1. Clone the repository.
2. Install the dependencies.
3. Ensure the required input CSV files are available in the expected directories.
4. Run `python pipeline.py`.
5. Inspect the generated files in `data/output/` and the execution log in `logs/run_log.txt`.

The pipeline uses the same documented cleaning, validation, and transformation steps for each run.