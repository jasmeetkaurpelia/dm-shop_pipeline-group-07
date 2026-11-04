# Cleaning Log

| Cleaning step | What changed | Why |
|---|---|---|
| Duplicate removal | Removed exact duplicate order rows | To prevent duplicate orders from being counted more than once |
| Text cleaning | Trimmed whitespace from text fields | To keep values consistent for validation and matching |
| Date parsing | Converted order dates into a consistent datetime format | To support date validation and date-based analysis |
| Numeric conversion | Converted quantity and unit price into numeric values | To enable validation and revenue calculations |
| Customer matching | Separated orders with unknown customer IDs | To prevent unmatched orders from entering the trusted dataset |
| Row quarantine | Separated rows with invalid or missing required values | To preserve problematic records without including them in trusted outputs |
| Source tracking | Added the source filename to each order | To trace records back to their original input file |
| Price standardisation | Converted March unit prices from cents to euros | To ensure prices use the same currency unit across all monthly files |
| Country standardisation | Corrected the known spelling error `Germny` to `Germany` | To ensure consistent country values |
| Email handling | Replaced the known malformed email with an empty value | The correct email could not be determined, so no address was invented |
| Cleaned customer output | Saved the cleaned customer master data as `clean_customers.csv` | To preserve and inspect cleaned customer records without modifying the raw input |