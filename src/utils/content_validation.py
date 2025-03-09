"""
Module for CSV content validation.

This module provides functionality for validating the content of CSV files,
focusing on the validation of individual data fields and row structures.
"""
import csv
import os
from datetime import datetime
from typing import List, Callable, Optional

from tqdm import tqdm  # Import tqdm for progress bars

from src.setup.setup import Setup
from src.utils.error_collector import ErrorCollector
from src.utils.footer_validation import FooterValidation
from src.utils.terminal_colors import TerminalColors
from src.utils.tqdm_config import custom_bar_format
from src.types.types import validators_pm10, validators_p20, validators_pm, validators_retour_pm, validators_retour_p20
# Import the validator classes directly to avoid circular imports
from src.utils.validators import (
    PM10Validation, P20Validation, PMValidation, 
    PMRetourValidation, P20RetourValidation
)


class ContentValidation:
    """
    Class for validating CSV file content.

    This class provides methods for validating the actual content
    of CSV files, excluding header and footer sections. It uses specialized
    validator classes for different record types (PM, PM_10, P_20).
    """

    def __init__(self):
        # Initialize Setup
        setup = Setup()
        # Import utf8 decoder
        self.encoding_to_utf8 = setup.encoding_to_utf8
        # define file for validation of iso2 format for code pays
        self.file_insee = "data/v_pays_territoire_2024.csv"
        # Get the base directory for reference files
        self.base_dir = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
        self.reference_file_path = os.path.join(self.base_dir, "data", "GD_Adresse_IP.csv")
        # Initialize content validators using the imported validator classes
        self.pm_content_validator = PMValidation()
        self.p20_content_validator = P20Validation()
        self.pm10_content_validator = PM10Validation()
        # Initialize retour validators
        self.pm_retour_validator = PMRetourValidation()
        self.p20_retour_validator = P20RetourValidation()
        self.validators_pm10 = validators_pm10
        self.validators_p20 = validators_p20
        self.validators_pm = validators_pm
        self.validators_retour_pm = validators_retour_pm
        self.validators_retour_p20 = validators_retour_p20

    def content_validation(self, total_lines, csv_reader, args, error_collector):
        """
        method for calling and organizing the aller file content validators
        """
        print(TerminalColors.section_header("VALIDATING LINES"))

        # Calculate number of data rows (total lines minus header)
        data_row_count = total_lines - 1

        # Process each data row in the CSV file
        for row_number, row in tqdm(
            enumerate(csv_reader, start=1),
            desc="Validating data rows",
            unit="rows",
            total=data_row_count,
            ncols=100,
            bar_format=custom_bar_format,
        ):
            # Strip whitespace from each field to avoid validation errors due to spacing
            fields = [field.strip() for field in row]

            # Route validation based on record type (first field of each row) and file type (aller or retour)
            if args.file_type == "aller":
                if fields[0] == "PM":
                    # Validate PM (Personne Morale) record structure for 'aller' file
                    self.pm_content_validator.validate_pm_structure(
                        fields, row_number, self.validators_pm, error_collector
                    )
                    # Store current PM ID for P_20 association
                    if len(fields) > 1:
                        self.p20_content_validator.current_pm_id = fields[1]
                elif fields[0] == "P_20":
                    # Validate P_20 (Address) record structure for 'aller' file
                    self.p20_content_validator.validate_p_20_structure(
                        fields, row_number, self.validators_p20, error_collector
                    )
                    # Validate P_20 against GD_Adresse_IP reference with correct reference file path
                    self.p20_content_validator.validate_gd_adresse_ip_reference(
                        fields, row_number, reference_file_path=self.reference_file_path, error_collector=error_collector
                    )
                elif fields[0] == "PM_10":
                    # Validate PM_10 (Business Activity) record structure for 'aller' file
                    self.pm10_content_validator.validate_pm_10_structure(
                        fields, row_number, self.validators_pm10, error_collector
                    )
                else:
                    # If not a recognized record type, assume it's a footer and validate accordingly
                    FooterValidation.validate_footer_structure(
                        csv_reader, fields, row_number, error_collector
                    )
            elif args.file_type == "retour":
                if fields[0] == "PM":
                    # Use the specialized RetourValidation for PM 'retour' structure
                    self.pm_retour_validator.validate_pm_retour_structure(
                        fields, row_number, self.validators_retour_pm, error_collector
                    )
                elif fields[0] == "P_20":
                    # Use the specialized RetourValidation for P_20 'retour' structure
                    self.p20_retour_validator.validate_p20_retour_structure(
                        fields, row_number, self.validators_retour_p20, error_collector
                    )
                elif fields[0] == "PM_10":
                    # For retour file, PM_10 uses the same validation as aller for now
                    self.pm10_content_validator.validate_pm_10_structure(
                        fields, row_number, self.validators_pm10, error_collector
                    )
                else:
                    # If not a recognized record type, assume it's a footer and validate accordingly
                    FooterValidation.validate_footer_structure(
                        csv_reader, fields, row_number, error_collector
                    )

        # After processing all rows, check P_20 ordering
        if args.file_type == "aller":
            self.p20_content_validator.validate_p20_ordering(error_collector)

    def validate_code_pays_insee_iso2(self, country_code: str) -> bool:
        """
        Validate country code against ISO2 format using INSEE reference data.

        Args:
            country_code: The country code to validate (ISO2 format)

        Returns:
            bool: True if the code exists in the INSEE reference data, False otherwise

        Note:
            This function checks against a reference file 'v_pays_territoire_2024.csv'
            which contains valid country codes in column 7.
        """
        with open(self.file_insee, encoding=self.encoding_to_utf8) as insee_file:
            insee_reader = csv.reader(insee_file)
            insee_header = next(insee_reader)
            if not insee_header:
                print("Error found in header. Content is empty")
                return False

            for insee_row in insee_reader:
                if insee_row[6].strip() == country_code:
                    return True
            return False
