"""
Main module for CSV file validation.

This module serves as the entry point for the table validation application,
orchestrating the validation process for CSV files by applying various
validation rules to headers, content rows, and footers.
"""
import csv  # Import CSV module to handle CSV file operations
import os   # Import OS module for file path operations
import sys  # Import SYS module for system-level operations

# Import validation modules from project structure
from src.types.utils.content_validation import ContentValidation
from src.types.utils.footer_validation import FooterValidation
from src.types.utils.header_validation import HeaderValidation
from src.types.utils.valid_pm_validation import ValidPmValidation
from src.utils.terminal_colors import TerminalColors

# Add the current directory to the system path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

# Open and process the CSV file using a context manager to ensure proper file handling
# The file is opened with UTF-8 encoding to properly handle special characters
with open("data/20250203T210108.csv", encoding="utf8") as file:
    # Create a CSV reader object with pipe ('|') as delimiter 
    reader = csv.reader(file, delimiter="|")
    
    # Read the first line of the CSV as the header
    header = next(reader)
    print(TerminalColors.info(f"Header: {TerminalColors.highlight_value('|'.join(header))}"))
    
    # Start header validation section
    print(TerminalColors.section_header("VALIDATING HEADER OF FILE"))
    
    # Validate the overall structure of the header (checking number of columns)
    HeaderValidation.HeaderStructureValidation.validate_number_of_columns(header)
    
    # Create a reference to the header field validation class for cleaner code
    header_field_validation = HeaderValidation.HeaderFieldValidation
    
    # Validate each field of the header according to specific rules
    # Field 0: Validate record type (must be 2 alphanumeric characters)
    if not header_field_validation.validate_varchar4_type_enregistrement(header[0]):
        print(TerminalColors.error(f"Invalid value {TerminalColors.highlight_value(header[0])}"))
    
    # Field 1: Validate extraction date (must match 'aller' format: yyyymmddhhmmss)
    if not header_field_validation.validate_date_extraction(header[1], "aller"):
        print(TerminalColors.error(f"Invalid value {TerminalColors.highlight_value(header[1])}"))
    
    # Field 2: Validate emitter (must be 6 alphabetic characters for 'aller' format)
    if not header_field_validation.validate_varchar6_emetteur(header[2], "aller"):
        print(TerminalColors.error(f"Invalid value {TerminalColors.highlight_value(header[2])}"))
    
    # Field 3: Validate version format (must start with 'V' followed by '1')
    if not header_field_validation.validate_str_plus_number_version(header[3]):
        print(TerminalColors.error(f"Invalid value {TerminalColors.highlight_value(header[3])}"))
    
    # End of header validation section
    print(TerminalColors.section_end())

    # Start data rows validation section
    print(TerminalColors.section_header("VALIDATING LINES"))
    
    # Process each data row in the CSV file
    for row_number, row in enumerate(reader):
        # Strip whitespace from each field to avoid validation errors due to spacing
        fields = [field.strip() for field in row]
        
        # Route validation based on record type (first field of each row)
        if fields[0] == "PM":
            # Validate PM (Personne Morale) record structure
            ContentValidation.PMValidation.validate_pm_structure(fields, row_number, validators_pm)
        elif fields[0] == "P_20":
            # Validate P_20 (Address) record structure
            ContentValidation.P20Validation.validate_p_20_structure(fields, row_number, validators_p20)
        elif fields[0] == "PM_10":
            # Validate PM_10 (Business Activity) record structure
            ContentValidation.PM10Validation.validate_pm_10_structure(fields, row_number, validators_pm10)
        else:
            # If not a recognized record type, assume it's a footer and validate accordingly
            FooterValidation.validate_footer_structure(reader, fields, row_number)
    
    # End of data rows validation section
    print(TerminalColors.section_end())
    
    # Start global PM table validation section
    print(TerminalColors.section_header("VALIDATING GLOBAL PM TABLE"))

    # Reuse the reader from previous steps for PM table validation
    reader_aller_file = reader
    
    # Perform global validation of PM table by comparing with reference data
    ValidPmValidation.import_pm_table(reader_aller_file)
    
    # End of global PM table validation section
    print(TerminalColors.section_end())

# Final message indicating completion of the validation process
print(TerminalColors.success("Validation complete."))
print(TerminalColors.section_end())
