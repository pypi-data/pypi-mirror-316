# Data Quality

This project provides a Data Quality Rule (DQR) enabler class for validating and reporting data quality metrics using Apache Spark and Jinja2. It allows users to perform various checks on a DataFrame, such as checking for null values, duplicates, uniqueness, range constraints, and values within a specific list. The results can be saved as an HTML report for easy review and sharing.

# Features

* Schema Validation : Compare the DataFrame's schema with an expected schema.
* Null Value Check : Identify the percentage of null values in specified columns.
* Duplicate Check : Find duplicate rows based on one or more columns.
* Uniqueness Check : Measure the uniqueness of values in specified columns.
* Range Check : Ensure column values fall within a defined range.
* Value Set Check : Verify if column values exist within a predefined list.
* HTML Report Generation : Automatically generate an HTML report summarizing all checks with visual tables.

# Installation

You can install the library using pip:

```bash
pip install dataquality_rules
```

