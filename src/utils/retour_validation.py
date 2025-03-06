"""
Module for 'retour' file format validation.

This module provides specialized validation for 'retour' file format,
which has a slightly different column structure compared to 'aller' format.
"""
from typing import List, Callable, Optional

from src.utils.content_validation import ContentValidation
from src.utils.error_collector import ErrorCollector


class RetourValidation:
    """
    Class for validating 'retour' file format.

    This class extends the functionality of ContentValidation with
    specialized methods for the 'retour' file format.
    """

    class PMRetourValidation:
        """
        Class for validating PM record types in 'retour' files.

        Provides additional validation methods specific to the PM
        record type in 'retour' file format.
        """

        @staticmethod
        def validate_column_retour_specific_field(field: str) -> bool:
            """
            Validates a retour-specific field that doesn't exist in 'aller' format.

            Args:
                field: The field value to validate

            Returns:
                bool: True if validation passes, False otherwise

            Note:
                This is a placeholder method. Implement specific validation
                rules based on the actual requirements for the field.
            """
            # Add specific validation rules based on requirements
            # For now, we just check if the field is not empty
            return field is not None and len(field) > 0

        @staticmethod
        def validate_pm_retour_structure(
                fields: List[str],
                row_number: int,
                validators: List[Callable[[str], bool]],
                error_collector: Optional[ErrorCollector] = None,
        ) -> None:
            """
            Validate PM record structure in 'retour' format.

            This method can be used instead of the standard validate_pm_structure
            if the retour PM format has structural differences that require
            special handling.

            Args:
                fields: List of field values from the row
                row_number: Row number for error reporting
                validators: List of validator functions to apply
                error_collector: Optional ErrorCollector instance to collect validation errors

            Returns:
                None. Validation errors are printed to console and/or added to error_collector.
            """
            content_validator = ContentValidation.PMValidation()
            # Use the existing PMValidation method or implement custom validation
            # For now, we're reusing the existing method
            content_validator.validate_pm_structure(
                fields, row_number, validators, error_collector
            )

    class P20RetourValidation:
        """
        Class for validating P_20 record types in 'retour' files.

        Provides additional validation methods specific to the P_20
        record type in 'retour' file format.
        """

        @staticmethod
        def validate_p20_retour_structure(
                fields: List[str],
                row_number: int,
                validators: List[Callable[[str], bool]],
                error_collector: Optional[ErrorCollector] = None,
        ) -> None:
            """
            Validate P_20 record structure in 'retour' format.

            This method can be used instead of the standard validate_p_20_structure
            if the retour P_20 format has structural differences that require
            special handling.

            Args:
                fields: List of field values from the row
                row_number: Row number for error reporting
                validators: List of validator functions to apply
                error_collector: Optional ErrorCollector instance to collect validation errors

            Returns:
                None. Validation errors are printed to console and/or added to error_collector.
            """
            content_validator = ContentValidation.P20Validation()
            # Use the existing P20Validation method or implement custom validation
            # For now, we're reusing the existing method
            content_validator.validate_p_20_structure(
                fields, row_number, validators, error_collector
            )
