"""
Main module for CSV file validation.

This module serves as the entry point for the table validation application,
orchestrating the validation process for CSV files by applying various
validation rules to headers, content rows, and footers.
"""
import csv  # Import CSV module to handle CSV file operations
import os  # Import OS module for file path operations
import sys  # Import SYS module for system-level operations

from tqdm import tqdm  # Import tqdm for progress bars

from src.setup.setup import Setup
from src.setup.teardown import Teardown
# Import validator lists from types
from src.utils.content_validation import ContentValidation
from src.utils.error_collector import ErrorCollector
# Import validation modules from project structure
from src.utils.header_validation import HeaderValidation
from src.utils.valid_pm_validation import ValidPmValidation
from src.utils.terminal_colors import TerminalColors

# Configure tqdm monitor
tqdm.monitor_interval = 0  # Disable monitor thread for better performance

# Add the current directory to the system path to ensure imports work correctly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))


def main():
    """Main function to run validation process."""
    # Initialize error collector
    error_collector = ErrorCollector()
    # Initialize setup
    setup = Setup()
    # Initialize header validator
    header_validator = HeaderValidation.HeaderStructureValidation()
    # Initialize Content validator
    content_validator = ContentValidation()
    # Initialize rp_validator
    rp_validator = ValidPmValidation()
    # Initialize teardown
    teardown = Teardown()

    try:
        # Parse command line arguments
        args = setup.argument_parser()
        
        # Fix file path if needed by checking if the file exists
        file_path = args.file
        if not os.path.exists(file_path):
            # Try with base directory
            base_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), args.file)
            if os.path.exists(base_path):
                file_path = base_path
            else:
                # Check if it's just in the 'data' folder without the 'data/' prefix
                if '/' in args.file:
                    _, filename = args.file.split('/', 1)
                    data_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'data', filename)
                    if os.path.exists(data_path):
                        file_path = data_path
        
        # Display some debug information about the file path
        print(TerminalColors.info(f"File path: {TerminalColors.highlight_value(file_path)}"))
        
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Cannot find file: {file_path}")
        
        # Get the total line count for progress reporting
        total_lines = setup.line_counter(args)
        
        # Open and process the CSV file using a context manager to ensure proper file handling
        # The file is opened with UTF-8 encoding to properly handle special characters
        with open(file_path, encoding=setup.encoding_to_utf8) as csv_file:
            # Create a CSV reader object with pipe ('|') as delimiter
            csv_reader = csv.reader(csv_file, delimiter=setup.aller_file_default_delimeter)

            # Read the first line of the CSV as the header
            header = setup.get_header(csv_reader)
            
            # Start header validation section
            header_validator.validate_header(header, args, error_collector)

            # Start data rows validation section
            content_validator.content_validation(
                total_lines, csv_reader, args, error_collector
            )

            # Start validation with RP data
            rp_validator.rp_validation(csv_file)

            # Doing the Teardown and showing result output
            teardown.generate_output(args, error_collector)
    
    except FileNotFoundError as e:
        print(TerminalColors.error(f"File Error: {e}"))
    except Exception as e:
        print(TerminalColors.error(f"An error occurred: {e}"))
        import traceback
        print(TerminalColors.error(traceback.format_exc()))


# Call the main function if this script is being run directly
if __name__ == "__main__":
    main()
