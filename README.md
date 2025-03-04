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
- **Multi-format support**: Handles both 'aller' and 'retour' file formats with different column structures

## Project Structure

```
tableValidation/
├── data/                   # Directory for CSV data files
├── src/
│   ├── types/
│   │   └── types.py        # Validator collections for different record types
│   └── utils/
│       ├── content_validation.py
│       ├── footer_validation.py
│       ├── header_validation.py
│       ├── retour_validation.py  # Specialized validation for 'retour' format
│       ├── valid_pm_validation.py
│       └── terminal_colors.py    # Terminal formatting utilities
└── main.py                 # Main entry point for validation
```

## Requirements

- Python 3.6+
- CSV files with specific format conforming to validation rules

## Usage

Place your CSV file in the data directory, then run:

```bash
python main.py --file path/to/your/file.csv --file-type [aller|retour] --format [terminal|html|json|all]
```

Command line arguments:
- `--file`: Path to the CSV file to validate (default: "data/20250203T210108.csv")
- `--file-type`: Type of file format to validate against (default: "aller")
- `--format`: Output format for validation results (default: "terminal")

The validation results will be displayed in the console with color-coded formatting for easy readability.

## File Format Support

The system supports two file formats:

### Aller Format

The original file format with standard structure and validation rules.

### Retour Format

A variant file format with slightly different column structure but sharing similar columns with the 'aller' format. The key differences include:
- Different date format in header (`yyyymmddThhmmss` instead of `yyyymmddhhmmss`)
- Different emitter format (7 alphabetic characters instead of 6)
- Different columns in PM and P_20 record types
- Custom validation rules for retour-specific fields

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

Each file format ('aller' or 'retour') uses its own set of validators that correspond to the specific column structure.

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

## Extending the System

To add support for additional file formats or new record types:

1. Create validator lists in `src/types/types.py`
2. Add specialized validation classes if needed (like `retour_validation.py`)
3. Update `main.py` to handle the new format or record type
4. Ensure proper validation rules are implemented
