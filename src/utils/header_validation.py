"""
Module for CSV header validation.

This module provides functionality for validating the structure and content
of CSV file headers according to specific format requirements.
"""
# Import datetime module for date format validation
from datetime import datetime

from src.utils.terminal_colors import TerminalColors


class HeaderValidation:
    """
    Class for validating CSV headers.

    This class provides methods and nested classes for validating both
    the structure and individual field contents of CSV file headers.
    """

    # Define validation for header
    class HeaderFieldValidation:
        """
        Class containing functions for validating individual header fields.

        Each method validates a specific type of header field according to
        format requirements such as length, type, and content patterns.
        """

        def __init__(self):
            self.expected_number_of_columns = 4

        @staticmethod
        def validate_varchar4_type_enregistrement(field: str) -> bool:
            """
            Check if field has exactly 2 alphanumeric characters.

            Args:
                field: The string field to validate

            Returns:
                bool: True if validation passes, False otherwise
            """
            # Validate that the field is exactly 2 characters long and only contains alphanumeric characters
            result = len(field) == 2 and field.isalnum()
            if result:
                print(
                    TerminalColors.success(
                        f"Header field 1 validation: {TerminalColors.highlight_value(field)} is valid"
                    )
                )
            else:
                print(
                    TerminalColors.error(
                        f"Header field 1 validation: {TerminalColors.highlight_value(field)}"
                        f" is invalid (expected 2 alphanumeric characters)"
                    )
                )
            return result

        @staticmethod
        def validate_date_extraction(field: str, aller_or_retour: str) -> bool:
            """
            Check if field has the required date format.

            Args:
                field: The date string to validate
                aller_or_retour: String indicating which format to validate against
                                ('aller' or 'retour')

            Returns:
                bool: True if validation passes, False otherwise

            Note:
                'aller' format is: yyyymmddhhmmss
                'retour' format is: yyyymmddThhmmss
            """
            # Different date format validation based on 'aller' or 'retour' parameter
            if aller_or_retour == "aller":
                try:
                    # Try to parse the date using the 'aller' format
                    datetime.strptime(field, "%Y%m%d%H%M%S")
                    print(
                        TerminalColors.success(
                            f"Header field 2 validation: {TerminalColors.highlight_value(field)}"
                            f" has valid 'aller' date format"
                        )
                    )
                    return True
                except ValueError:
                    # Return False if the date string can't be parsed according to the format
                    print(
                        TerminalColors.error(
                            f"Header field 2 validation: {TerminalColors.highlight_value(field)}"
                            f" has invalid 'aller' date format (expected yyyymmddhhmmss)"
                        )
                    )
                    return False
            elif aller_or_retour == "retour":
                try:
                    # Try to parse the date using the 'retour' format (with 'T' separator)
                    datetime.strptime(field, "%Y%m%dT%H%M%S")
                    print(
                        TerminalColors.success(
                            f"Header field 2 validation: {TerminalColors.highlight_value(field)}"
                            f" has valid 'retour' date format"
                        )
                    )
                    return True
                except ValueError:
                    # Return False if the date string can't be parsed according to the format
                    print(
                        TerminalColors.error(
                            f"Header field 2 validation: {TerminalColors.highlight_value(field)}"
                            f" has invalid 'retour' date format (expected yyyymmddThhmmss)"
                        )
                    )
                    return False
            else:
                return False

        @staticmethod
        def validate_varchar6_emetteur(field: str, aller_or_retour: str) -> bool:
            """
            Check if field has the required number of alphabetic characters.

            Args:
                field: The string field to validate
                aller_or_retour: String indicating which validation rules to apply
                                ('aller' or 'retour')

            Returns:
                bool: True if validation passes, False otherwise

            Note:
                'aller' requires exactly 6 alphabetic characters
                'retour' requires exactly 7 alphabetic characters
            """
            # Different length validation based on 'aller' or 'retour' parameter
            if aller_or_retour == "aller":
                # For 'aller', validate that the field is exactly 6 characters and only alphabetic
                result = len(field) == 6 and field.isalpha()
                if result:
                    print(
                        TerminalColors.success(
                            f"Header field 3 validation: {TerminalColors.highlight_value(field)}"
                            f" is valid for 'aller' format"
                        )
                    )
                else:
                    print(
                        TerminalColors.error(
                            f"Header field 3 validation: {TerminalColors.highlight_value(field)}"
                            f" is invalid for 'aller' format (expected 6 alphabetic characters)"
                        )
                    )
                return result
            elif aller_or_retour == "retour":
                # For 'retour', validate that the field is exactly 7 characters and only alphabetic
                result = len(field) == 7 and field.isalpha()
                if result:
                    print(
                        TerminalColors.success(
                            f"Header field 3 validation: {TerminalColors.highlight_value(field)}"
                            f" is valid for 'retour' format"
                        )
                    )
                else:
                    print(
                        TerminalColors.error(
                            f"Header field 3 validation: {TerminalColors.highlight_value(field)}"
                            f" is invalid for 'retour' format (expected 7 alphabetic characters)"
                        )
                    )
                return result
            else:
                return False

        @staticmethod
        def validate_str_plus_number_version(field: str) -> bool:
            """
            Check if field starts with 'V' and is followed by '1'.

            Args:
                field: The string field to validate

            Returns:
                bool: True if validation passes, False otherwise
            """
            # Check that the field starts with 'V' at position 0 and has '1' at position 1
            result = field[0] == "V" and field[1] == "1"
            if result:
                print(
                    TerminalColors.success(
                        f"Header field 4 validation: {TerminalColors.highlight_value(field)} is valid"
                    )
                )
            else:
                print(
                    TerminalColors.error(
                        f"Header field 4 validation: {TerminalColors.highlight_value(field)}"
                        f" is invalid (expected format V1*)"
                    )
                )
            return result

    class HeaderStructureValidation:
        """
        Class for validating the overall structure of CSV headers.

        Provides methods to validate header elements like column count
        and general format requirements.
        """

        def __init__(self):
            self.expected_number_of_columns = 4

        def validate_header(self, header, args, error_collector):
            """
            caller to validate the header
            """
            print(TerminalColors.section_header("VALIDATING HEADER OF FILE"))
            # Validate the overall structure of the header (checking number of columns)
            header_validator = HeaderValidation.HeaderStructureValidation()
            if not header_validator.validate_number_of_columns(header):
                error_collector.add_error(
                    "header",
                    "structure",
                    "columns",
                    f"Invalid number of columns: {len(header)} (expected {self.expected_number_of_columns})",
                )
            # Validate each field of the header according to specific rules
            # Field 0: Validate record type (must be 2 alphanumeric characters)
            header_field_validator = HeaderValidation.HeaderFieldValidation()
            if not header_field_validator.validate_varchar4_type_enregistrement(
                    header[0]
            ):
                error_collector.add_error(
                    "header", "format", "record_type", f"Invalid value {header[0]}"
                )

            # Field 1: Validate extraction date based on file type
            if not header_field_validator.validate_date_extraction(
                    header[1], args.file_type
            ):
                error_collector.add_error(
                    "header", "format", "extraction_date", f"Invalid value {header[1]}"
                )

            # Field 2: Validate emitter based on file type
            if not header_field_validator.validate_varchar6_emetteur(
                    header[2], args.file_type
            ):
                error_collector.add_error(
                    "header", "format", "emitter", f"Invalid value {header[2]}"
                )

            # Field 3: Validate version format (must start with 'V' followed by '1')
            if not header_field_validator.validate_str_plus_number_version(header[3]):
                error_collector.add_error(
                    "header", "format", "version", f"Invalid value {header[3]}"
                )
            # End of header validation section
            print(TerminalColors.section_end())

        def validate_number_of_columns(self, header: list[str]) -> bool:
            """
            Validates the number of columns equals 4.

            Args:
                header: The list of header columns to validate

            Returns:
                None
            """
            # Check if the header has exactly 4 columns, print error message if not
            if len(header) != self.expected_number_of_columns:
                print(
                    TerminalColors.error(
                        f"Invalid number of columns in header: "
                        f"{TerminalColors.highlight_value(str(len(header)))}"
                        f" (expected {self.expected_number_of_columns})"
                    )
                )
                return False
            else:
                print(
                    TerminalColors.success(
                        f"Header column count: {TerminalColors.highlight_value(str(len(header)))} is valid"
                    )
                )
                return True
