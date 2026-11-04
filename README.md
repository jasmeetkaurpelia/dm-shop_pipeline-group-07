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
├── data/
│   ├── raw/
│   │   ├── customers.csv
│   │   ├── orders_2026_01.csv
│   │   ├── orders_2026_02.csv
│   │   └── orders_2026_03.csv
│   └── output/
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

### `fct_orders.csv`

Contains trusted order records ready for analysis.

| Column | Description | Unit / Rule |
|---|---|---|
| `order_id` | Order identifier | One capital letter followed by three digits; unique |
| `order_date` | Order date | YYYY-MM-DD |
| `customer_id` | Customer identifier | Must exist in customer data |
| `category` | Product category | Accessories or Electronics |
| `quantity` | Number of items ordered | Greater than 0 |
| `unit_price` | Price per item | EUR, greater than or equal to 0 |
| `source_file` | Original input filename | Data lineage |
| `city` | Customer's city | Retrieved