"""
Main module for CSV file validation.

This module serves as the entry point for the table validation application,
orchestrating the validation process for CSV files by applying various
validation rules to headers, content rows, and footers.
"""
import csv  # Import CSV module to handle CSV file operations
import os   # Import OS module for file path operations
import sys  # Import SYS module for system-level operations
import argparse  # Import for command line argument parsing

# Import validation modules from project structure
from src.types.utils.content_validation import ContentValidation
from src.types.utils.footer_validation import FooterValidation
from src.types.utils.header_validation import HeaderValidation
from src.types.utils.valid_pm_validation import ValidPmValidation
from src.utils.terminal_colors import TerminalColors
from src.utils.error_collector import ErrorCollector

# Add the current directory to the system path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Main function to run validation process."""
    # Parse command line arguments
    parser = argparse.ArgumentParser(description='CSV Table Validation Tool')
    parser.add_argument('--file', type=str, default="data/20250203T210108.csv",
                        help='Path to the CSV file to validate')
    parser.add_argument('--format', type=str, choices=['terminal', 'html', 'json', 'all'],
                        default='terminal', help='Output format for validation results')
    args = parser.parse_args()
    
    # Initialize error collector
    error_collector = ErrorCollector()
    
    # Open and process the CSV file using a context manager to ensure proper file handling
    # The file is opened with UTF-8 encoding to properly handle special characters
    with open(args.file, encoding="utf8") as file:
        # Create a CSV reader object with pipe ('|') as delimiter 
        reader = csv.reader(file, delimiter="|")
        
        # Read the first line of the CSV as the header
        header = next(reader)
        print(TerminalColors.info(f"Header: {TerminalColors.highlight_value('|'.join(header))}"))
        
        # Start header validation section
        print(TerminalColors.section_header("VALIDATING HEADER OF FILE"))
        
        # Validate the overall structure of the header (checking number of columns)
        if not HeaderValidation.HeaderStructureValidation.validate_number_of_columns(header):
            error_collector.add_error('header', 'structure', 'columns', 
                                     f"Invalid number of columns: {len(header)} (expected specific number)")
        
        # Create a reference to the header field validation class for cleaner code
        header_field_validation = HeaderValidation.HeaderFieldValidation
        
        # Validate each field of the header according to specific rules
        # Field 0: Validate record type (must be 2 alphanumeric characters)
        if not header_field_validation.validate_varchar4_type_enregistrement(header[0]):
            error_collector.add_error('header', 'format', 'record_type', 
                                    f"Invalid value {header[0]}")
        
        # Field 1: Validate extraction date (must match 'aller' format: yyyymmddhhmmss)
        if not header_field_validation.validate_date_extraction(header[1], "aller"):
            error_collector.add_error('header', 'format', 'extraction_date', 
                                     f"Invalid value {header[1]}")
        
        # Field 2: Validate emitter (must be 6 alphabetic characters for 'aller' format)
        if not header_field_validation.validate_varchar6_emetteur(header[2], "aller"):
            error_collector.add_error('header', 'format', 'emitter', 
                                     f"Invalid value {header[2]}")
        
        # Field 3: Validate version format (must start with 'V' followed by '1')
        if not header_field_validation.validate_str_plus_number_version(header[3]):
            error_collector.add_error('header', 'format', 'version', 
                                     f"Invalid value {header[3]}")
        
        # End of header validation section
        print(TerminalColors.section_end())

        # Start data rows validation section
        print(TerminalColors.section_header("VALIDATING LINES"))
        
        # Define validation functions for different record types
        validators_pm = [...]  # Define your validators here or import them
        validators_p20 = [...]  # Define your validators here or import them
        validators_pm10 = [...]  # Define your validators here or import them
        
        # Create collector functions to capture errors instead of printing
        def pm_structure_validator(fields, row_number, validators):
            if len(fields) != expected_pm_columns:  # Replace with your expected column count
                error_collector.add_error('content', 'structure', 'PM',
                                         f"Invalid number of columns: {len(fields)} (expected {expected_pm_columns})",
                                         row=row_number)
            
            # Validate each field
            for i, (validator, field) in enumerate(zip(validators, fields)):
                if not validator(field):
                    error_collector.add_error('content', 'format', f'PM_Column{i+1}',
                                            f"Invalid value '{field}'. Validate rules for column",
                                            row=row_number)
        
        def p20_structure_validator(fields, row_number, validators):
            if len(fields) != expected_p20_columns:  # Replace with your expected column count
                error_collector.add_error('content', 'structure', 'P_20',
                                         f"Invalid number of columns: {len(fields)} (expected {expected_p20_columns})",
                                         row=row_number)
            
            # Validate each field
            for i, (validator, field) in enumerate(zip(validators, fields)):
                if not validator(field):
                    error_collector.add_error('content', 'format', f'P20_Column{i+1}',
                                            f"Invalid value '{field}'. Validate rules for column",
                                            row=row_number)
        
        def pm10_structure_validator(fields, row_number, validators):
            if len(fields) != expected_pm10_columns:  # Replace with your expected column count
                error_collector.add_error('content', 'structure', 'PM_10',
                                         f"Invalid number of columns: {len(fields)} (expected {expected_pm10_columns})",
                                         row=row_number)
            
            # Validate each field
            for i, (validator, field) in enumerate(zip(validators, fields)):
                if not validator(field):
                    error_collector.add_error('content', 'format', f'PM10_Column{i+1}',
                                            f"Invalid value '{field}'. Validate rules for column",
                                            row=row_number)
        
        # Define expected column counts
        expected_pm_columns = 5  # Replace with your expected column count
        expected_p20_columns = 10  # Replace with your expected column count
        expected_pm10_columns = 5  # Replace with your expected column count
        
        # Process each data row in the CSV file
        for row_number, row in enumerate(reader, start=1):
            # Strip whitespace from each field to avoid validation errors due to spacing
            fields = [field.strip() for field in row]
            
            # Route validation based on record type (first field of each row)
            if fields[0] == "PM":
                # Validate PM (Personne Morale) record structure
                pm_structure_validator(fields, row_number, validators_pm)
            elif fields[0] == "P_20":
                # Validate P_20 (Address) record structure
                p20_structure_validator(fields, row_number, validators_p20)
            elif fields[0] == "PM_10":
                # Validate PM_10 (Business Activity) record structure
                pm10_structure_validator(fields, row_number, validators_pm10)
            else:
                # If not a recognized record type, assume it's a footer and validate accordingly
                # Modify footer validation to use error collector
                def footer_validator(reader, fields, row_number):
                    # Add your footer validation logic here
                    # Example:
                    if len(fields) != expected_footer_columns:  # Replace with your expected column count
                        error_collector.add_error('footer', 'structure', 'Footer',
                                                f"Invalid number of columns: {len(fields)} (expected {expected_footer_columns})",
                                                row=row_number)
                
                footer_validator(reader, fields, row_number)
        
        # End of data rows validation section
        print(TerminalColors.section_end())
        
        # Start global PM table validation section
        print(TerminalColors.section_header("VALIDATING GLOBAL PM TABLE"))

        # Reuse the reader from previous steps for PM table validation
        reader_aller_file = reader
        
        # Perform global validation of PM table by comparing with reference data
        # Modify to use error collector
        def pm_table_validator(reader_aller_file):
            # Add your PM table validation logic here
            # Use error_collector.add_error() when validation fails
            pass
        
        pm_table_validator(reader_aller_file)
        
        # End of global PM table validation section
        print(TerminalColors.section_end())

    # Generate appropriate output based on format argument
    if args.format == 'terminal' or args.format == 'all':
        error_collector.print_terminal_report()
    
    if args.format == 'html' or args.format == 'all':
        html_path = error_collector.generate_html_report()
        print(f"\nHTML report generated: {html_path}")
    
    if args.format == 'json' or args.format == 'all':
        json_path = error_collector.export_json()
        print(f"\nJSON export generated: {json_path}")
    
    # Final message indicating completion of the validation process
    print(TerminalColors.success("Validation complete."))
    print(TerminalColors.section_end())

if __name__ == "__main__":
    main()
