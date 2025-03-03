# CSV Table Validation Framework

A robust Python framework for validating CSV files with structured validation across multiple components.

## Overview

This project provides a comprehensive validation system for CSV files, focusing on validating different structural components:

- **Header validation**: Ensures the CSV header meets specific format requirements
- **Content validation**: Validates data rows in the CSV based on record types (PM, P_20, PM_10)
- **Footer validation**: Validates the footer section of the CSV file
- **PM validation**: Performs additional validation for PM (Personne Morale) records against reference data

The framework includes terminal colorization and formatting to improve the visibility of testing steps without cluttering the output.

## Features

- **Multi-component validation**: Separates validation concerns for headers, content rows, and footers
- **Type-specific validation**: Handles different record types with specialized validation rules
- **Reference data validation**: Compares data against external reference files
- **Terminal colorization**: Enhances output readability with colored formatting
- **Structured output**: Organizes validation results into clear sections

## Project Structure

```
tableValidation/
├── data/                   # Directory for CSV data files
├── src/
│   ├── types/
│   │   └── utils/          # Validation utilities for different components
│   │       ├── content_validation.py
│   │       ├── footer_validation.py
│   │       ├── header_validation.py
│   │       └── valid_pm_validation.py
│   └── utils/
│       └── terminal_colors.py  # Terminal formatting utilities
└── main.py                 # Main entry point for validation
```

## Requirements

- Python 3.6+
- CSV files with specific format conforming to validation rules

## Usage

Place your CSV file in the data directory with the appropriate name, then run:

```bash
python main.py
```

The validation results will be displayed in the console with color-coded formatting for easy readability.

## Validation Components

### Header Validation

Validates the structure and content of CSV headers, including:
- Number of columns
- Record type format (2 alphanumeric characters)
- Extraction date format (yyyymmddhhmmss for 'aller', yyyymmddThhmmss for 'retour')
- Emitter format (6 alphabetic characters for 'aller', 7 for 'retour')
- Version format (starts with 'V' followed by '1')

### Content Validation

Validates data rows based on their record type:
- PM (Personne Morale) records
- P_20 (Address) records
- PM_10 (Business Activity) records

### PM Validation

Performs comprehensive validation of PM records by:
- Importing and filtering reference data
- Comparing PM records against reference data
- Bidirectional validation (both forward and reverse)
- Generating statistical summaries of validation results

## Output Formatting

The framework uses terminal colorization to enhance readability:
- **Blue background**: Section headers and separators
- **Green**: Success messages
- **Red**: Error messages
- **Yellow**: Warning messages and highlighted values
- **Cyan**: Informational messages
- **Magenta**: Processing status messages

## Testing

Tests are implemented using pytest. To run the tests:

```bash
pytest
```
