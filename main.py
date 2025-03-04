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
from typing import List, Callable, Iterator
from tqdm import tqdm  # Import tqdm for progress bars
from src.utils.tqdm_config import custom_bar_format  # Import the custom bar format

# Import validation modules from project structure
from src.utils.header_validation import HeaderValidation
from src.utils.terminal_colors import TerminalColors
from src.utils.error_collector import ErrorCollector
from src.utils.valid_pm_validation import ValidPmValidation
from src.utils.footer_validation import FooterValidation
from src.utils.content_validation import ContentValidation
from src.utils.retour_validation import RetourValidation  # Import the new RetourValidation class
# Import validator lists from types
from src.types.types import (
    validators_pm, validators_p20, validators_pm10,
    validators_retour_pm, validators_retour_p20
)

# Configure tqdm monitor
tqdm.monitor_interval = 0  # Disable monitor thread for better performance

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
    parser.add_argument('--file-type', type=str, choices=['aller', 'retour'],
                        default='aller', help='Type of file format (aller or retour)')
    args = parser.parse_args()
    
    # Initialize error collector
    error_collector = ErrorCollector()
    
    # Get the total line count for progress reporting
    total_lines = sum(1 for _ in open(args.file, encoding="utf8"))
    print(TerminalColors.info(f"Processing file with {TerminalColors.highlight_value(str(total_lines))} lines"))
    print(TerminalColors.info(f"File type: {TerminalColors.highlight_value(args.file_type)}"))
    
    # Open and process the CSV file using a context manager to ensure proper file handling
    # The file is opened with UTF-8 encoding to properly handle special characters
    with open(args.file, encoding="utf8") as csv_file:
        # Create a CSV reader object with pipe ('|') as delimiter 
        csv_reader = csv.reader(csv_file, delimiter="|")
        
        # Read the first line of the CSV as the header
        header = next(csv_reader)
        print(TerminalColors.info(f"Header: {TerminalColors.highlight_value('|'.join(header))}"))
        
        # Start header validation section
        print(TerminalColors.section_header("VALIDATING HEADER OF FILE"))
        
        # Validate the overall structure of the header (checking number of columns)
        if not HeaderValidation.HeaderStructureValidation.validate_number_of_columns(header):
            error_collector.add_error('header', 'structure', 'columns', 
                                     f"Invalid number of columns: {len(header)} (expected specific number)")
        
        header_field_validation = HeaderValidation.HeaderFieldValidation
        
        # Validate each field of the header according to specific rules
        # Field 0: Validate record type (must be 2 alphanumeric characters)
        if not header_field_validation.validate_varchar4_type_enregistrement(header[0]):
            error_collector.add_error('header', 'format', 'record_type', 
                                    f"Invalid value {header[0]}")
        
        # Field 1: Validate extraction date based on file type
        if not header_field_validation.validate_date_extraction(header[1], args.file_type):
            error_collector.add_error('header', 'format', 'extraction_date', 
                                     f"Invalid value {header[1]}")
        
        # Field 2: Validate emitter based on file type
        if not header_field_validation.validate_varchar6_emetteur(header[2], args.file_type):
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
        
        # Calculate number of data rows (total lines minus header)
        data_row_count = total_lines - 1
        
        # Process each data row in the CSV file
        for row_number, row in tqdm(enumerate(csv_reader, start=1), 
                                   desc="Validating data rows", 
                                   unit="rows",
                                   total=data_row_count,
                                   ncols=100,
                                   bar_format=custom_bar_format):
            # Strip whitespace from each field to avoid validation errors due to spacing
            fields = [field.strip() for field in row]
            
            # Route validation based on record type (first field of each row) and file type (aller or retour)
            if args.file_type == 'aller':
                if fields[0] == "PM":
                    # Validate PM (Personne Morale) record structure for 'aller' file
                    ContentValidation.PMValidation.validate_pm_structure(fields, row_number, validators_pm, error_collector)
                elif fields[0] == "P_20":
                    # Validate P_20 (Address) record structure for 'aller' file
                    ContentValidation.P20Validation.validate_p_20_structure(fields, row_number, validators_p20, error_collector)
                elif fields[0] == "PM_10":
                    # Validate PM_10 (Business Activity) record structure for 'aller' file
                    ContentValidation.PM10Validation.validate_pm_10_structure(fields, row_number, validators_pm10, error_collector)
                else:
                    # If not a recognized record type, assume it's a footer and validate accordingly
                    FooterValidation.validate_footer_structure(csv_reader, fields, row_number, error_collector)
            elif args.file_type == 'retour':
                if fields[0] == "PM":
                    # Use the specialized RetourValidation for PM 'retour' structure
                    RetourValidation.PMRetourValidation.validate_pm_retour_structure(
                        fields, row_number, validators_retour_pm, error_collector
                    )
                elif fields[0] == "P_20":
                    # Use the specialized RetourValidation for P_20 'retour' structure
                    RetourValidation.P20RetourValidation.validate_p20_retour_structure(
                        fields, row_number, validators_retour_p20, error_collector
                    )
                elif fields[0] == "PM_10":
                    # For retour file, PM_10 uses the same validation as aller for now
                    ContentValidation.PM10Validation.validate_pm_10_structure(fields, row_number, validators_pm10, error_collector)
                else:
                    # If not a recognized record type, assume it's a footer and validate accordingly
                    FooterValidation.validate_footer_structure(csv_reader, fields, row_number, error_collector)
        
        # End of data rows validation section
        print(TerminalColors.section_end())
        
        # Start global PM table validation section
        print(TerminalColors.section_header("VALIDATING GLOBAL PM TABLE"))

        # Reset file pointer to beginning for PM table validation
        csv_file.seek(0)
        pm_validation_reader = csv.reader(csv_file, delimiter="|")
        # Skip header row that we already processed
        next(pm_validation_reader)
        
        # Perform global validation of PM table by comparing with reference data
        def validate_pm_table(pm_reader: Iterator[List[str]]):
            # Call the ValidPmValidation.import_pm_table method to 
            # validate the PM table data against reference files
            ValidPmValidation.import_pm_table(pm_reader)
            # Any errors found by the import_pm_table method will be printed directly
        
        validate_pm_table(pm_validation_reader)
        
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
