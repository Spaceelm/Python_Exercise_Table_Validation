"""
Validator classes for CSV data validation.

This module provides validator classes for different types of CSV records (PM, P_20, PM_10).
These classes define validation methods for each field in the records.
"""
import re
from datetime import datetime
from typing import Optional, List, Callable

# Import ErrorCollector type for type hints
from src.utils.error_collector import ErrorCollector


class PMValidation:
    """
    Validation class for PM (Personne Morale) records.
    
    This class provides validation methods for each field in PM records.
    """
    
    def __init__(self):
        """Initialize PM validator with any necessary configuration."""
        self.expected_number_columns = 16
    
    @staticmethod
    def validate_column1_type_enregistrement(field: str) -> bool:
        """Validate record type (must be PM, P_20, or PM_10)."""
        return field in ["PM", "P_20", "PM_10"]
    
    @staticmethod
    def validate_column2_id_stable(field: str) -> bool:
        """Validate stable ID (must be alphanumeric and of appropriate length)."""
        return bool(re.match(r'^[A-Za-z0-9]+$', field)) and len(field) <= 128
    
    @staticmethod
    def validate_column3_uuid(field: str) -> bool:
        """Validate UUID format."""
        return bool(re.match(r'^[A-Za-z0-9\-]+$', field)) and len(field) <= 36
    
    @staticmethod
    def validate_column4_network(field: str) -> bool:
        """Validate network code."""
        return bool(re.match(r'^[A-Z0-9]+$', field)) and len(field) <= 10
    
    @staticmethod
    def validate_column5_denomination_social(field: str) -> bool:
        """Validate company name (must be 250 characters or fewer)."""
        return len(field) <= 250
    
    @staticmethod
    def validate_column6_siren(field: str) -> bool:
        """Validate SIREN number (must be 18 characters or fewer)."""
        return len(field) <= 18
    
    @staticmethod
    def validate_column7_siret(field: str) -> bool:
        """Validate SIRET number (must be 18 characters or fewer)."""
        return len(field) <= 18
    
    @staticmethod
    def validate_column8_type_other_immatriculation(field: str) -> bool:
        """Validate other registration type (must be 18 characters or fewer)."""
        return len(field) <= 18
    
    @staticmethod
    def validate_column9_autre_immatriculation(field: str) -> bool:
        """Validate other registration number (must be 128 characters or fewer)."""
        return len(field) <= 128
    
    @staticmethod
    def validate_column10_identifiant_rna(field: str) -> bool:
        """Validate RNA identifier (must be 10 characters or fewer)."""
        return len(field) <= 10
    
    @staticmethod
    def validate_column11_autre_numero_association(field: str) -> bool:
        """Validate other association number (must be 128 characters or fewer)."""
        return len(field) <= 128
    
    @staticmethod
    def validate_column12_code_categorie_juridique(field: str) -> bool:
        """Validate legal category code (must be 128 characters or fewer)."""
        return len(field) <= 128
    
    @staticmethod
    def validate_column13_code_pays_enregistrement(field: str) -> bool:
        """Validate country code (must be valid ISO2 format)."""
        return bool(re.match(r'^[A-Z]{2}$', field)) or not field
    
    @staticmethod
    def validate_column14_resultat_verification(field: str) -> bool:
        """Validate verification result (must be 128 characters or fewer)."""
        return len(field) <= 128
    
    @staticmethod
    def validate_column15_date_derniere_verification(field: str) -> bool:
        """Validate last verification date (must be in valid date format or empty)."""
        if not field:
            return True
        try:
            datetime.strptime(field, "%Y-%m-%d")
            return True
        except ValueError:
            return False
    
    @staticmethod
    def validate_column16_date_evolution_pm_chez_cardif(field: str) -> bool:
        """Validate PM evolution date (must be in valid date format or empty)."""
        if not field:
            return True
        try:
            datetime.strptime(field, "%Y-%m-%d")
            return True
        except ValueError:
            return False
            
    def validate_pm_structure(
            self,
            fields: List[str],
            row_number: int,
            validators_for_pm: List[Callable[[str], bool]],
            error_collector: Optional[ErrorCollector] = None,
    ) -> None:
        """
        Validate PM record structure and field formats.

        Args:
            fields: List of field values from the row
            row_number: Row number for error reporting
            validators_for_pm: List of validator functions to apply
            error_collector: Optional ErrorCollector instance to collect validation errors

        Returns:
            None. Validation errors are printed to console and/or added to error_collector.
        """
        # Check the number of columns
        if len(fields) != self.expected_number_columns:
            if error_collector:
                error_collector.add_error(
                    "content",
                    "structure",
                    "PM",
                    f"Invalid number of columns: {len(fields)} (expected {self.expected_number_columns})",
                    row=row_number,
                )
            else:
                print(
                    f"Row {row_number}: Invalid number of columns: {len(fields)}"
                    f" (expected {self.expected_number_columns})"
                )

        # Validate each field
        for i, (validator, field) in enumerate(zip(validators_for_pm, fields)):
            if not validator(field):
                if error_collector:
                    error_collector.add_error(
                        "content",
                        "format",
                        f"PM_Column{i + 1}",
                        f"Invalid value '{field}'. Validate rules for column",
                        row=row_number,
                    )
                else:
                    print(
                        f"[PM] Row {row_number}, Column{i + 1}: Invalid value '{field}'. Validate rules for column"
                    )


class P20Validation:
    """
    Validation class for P_20 (Address) records.
    
    This class provides validation methods for each field in P_20 records.
    """
    
    def __init__(self):
        """Initialize P20 validator with any necessary configuration."""
        self.expected_number_columns = 14
    
    @staticmethod
    def validate_column5_l1_address(field: str) -> bool:
        """Validate address line 1 (must be 128 characters or fewer)."""
        return len(field) <= 128
    
    @staticmethod
    def validate_column6_l2_address(field: str) -> bool:
        """Validate address line 2 (must be 128 characters or fewer)."""
        return len(field) <= 128
    
    @staticmethod
    def validate_column7_l3_address(field: str) -> bool:
        """Validate address line 3 (must be 128 characters or fewer)."""
        return len(field) <= 128
    
    @staticmethod
    def validate_column8_l4_address(field: str) -> bool:
        """Validate address line 4 (must be 128 characters or fewer)."""
        return len(field) <= 128
    
    @staticmethod
    def validate_column9_l5_adresse(field: str) -> bool:
        """Validate address line 5 (must be 128 characters or fewer)."""
        return len(field) <= 128
    
    @staticmethod
    def validate_column10_l6_adresse(field: str) -> bool:
        """Validate address line 6 (must be 128 characters or fewer)."""
        return len(field) <= 128
    
    @staticmethod
    def validate_column11_code_postal(field: str) -> bool:
        """Validate postal code (must be 128 characters or fewer)."""
        return len(field) <= 128
    
    @staticmethod
    def validate_column12_commune(field: str) -> bool:
        """Validate city/town (must be 128 characters or fewer)."""
        return len(field) <= 128
    
    @staticmethod
    def validate_column13_state(field: str) -> bool:
        """Validate state/province (must be 10 characters or fewer)."""
        return len(field) <= 10
    
    @staticmethod
    def validate_column14_pays(field: str) -> bool:
        """Validate country (must be valid ISO2 format)."""
        return bool(re.match(r'^[A-Z]{2}$', field)) or not field
        
    def validate_p_20_structure(
            self,
            fields: List[str],
            row_number: int,
            validators_for_p20: List[Callable[[str], bool]],
            error_collector: Optional[ErrorCollector] = None,
    ) -> None:
        """
        Validate P_20 record structure and field formats.

        Args:
            fields: List of field values from the row
            row_number: Row number for error reporting
            validators_for_p20: List of validator functions to apply
            error_collector: Optional ErrorCollector instance to collect validation errors

        Returns:
            None. Validation errors are printed to console and/or added to error_collector.
        """
        # Check the number of columns
        if len(fields) != self.expected_number_columns:
            if error_collector:
                error_collector.add_error(
                    "content",
                    "structure",
                    "P_20",
                    f"Invalid number of columns: {len(fields)} (expected {self.expected_number_columns})",
                    row=row_number,
                )
            else:
                print(
                    f"Row {row_number}: Invalid number of columns: {len(fields)}"
                    f" (expected {self.expected_number_columns})"
                )

        # Validate each field
        for i, (validator, field) in enumerate(zip(validators_for_p20, fields)):
            if not validator(field):
                if error_collector:
                    error_collector.add_error(
                        "content",
                        "format",
                        f"P_20_Column{i + 1}",
                        f"Invalid value '{field}'. Validate rules for column",
                        row=row_number,
                    )
                else:
                    print(
                        f"[P_20] Row {row_number}, Column{i + 1}: Invalid value '{field}'. Validate rules for column"
                    )


class PM10Validation:
    """
    Validation class for PM_10 (Business Activity) records.
    
    This class provides validation methods for each field in PM_10 records.
    """
    
    def __init__(self):
        """Initialize PM10 validator with any necessary configuration."""
        self.expected_number_columns = 5
    
    @staticmethod
    def validate_column5_code_ape(field: str) -> bool:
        """Validate APE code (must be 128 characters or fewer)."""
        return len(field) <= 128
        
    def validate_pm_10_structure(
            self,
            fields: List[str],
            row_number: int,
            validators_for_pm10: List[Callable[[str], bool]],
            error_collector: Optional[ErrorCollector] = None,
    ) -> None:
        """
        Validate PM_10 record structure and field formats.

        Args:
            fields: List of field values from the row
            row_number: Row number for error reporting
            validators_for_pm10: List of validator functions to apply
            error_collector: Optional ErrorCollector instance to collect validation errors

        Returns:
            None. Validation errors are printed to console and/or added to error_collector.
        """
        # Check the number of columns
        if len(fields) != self.expected_number_columns:
            if error_collector:
                error_collector.add_error(
                    "content",
                    "structure",
                    "PM_10",
                    f"Invalid number of columns: {len(fields)}"
                    f" (expected {self.expected_number_columns})",
                    row=row_number,
                )
            else:
                print(
                    f"Row {row_number}: "
                    f"Invalid number of columns: {len(fields)}"
                    f" (expected {self.expected_number_columns})"
                )

        # Validate each field
        for i, (validator, field_tuple) in enumerate(
                zip(validators_for_pm10, fields)
        ):
            if not validator(field_tuple):
                if error_collector:
                    error_collector.add_error(
                        "content",
                        "format",
                        f"PM_10_Column{i + 1}",
                        f"Invalid value '{field_tuple}'. Validate rules for column",
                        row=row_number,
                    )
                else:
                    print(
                        f"[PM_10] Row {row_number}, "
                        f"Column{i + 1}: "
                        f"Invalid value '{field_tuple}'. "
                        f"Validate rules for column"
                    )


class PMRetourValidation:
    """
    Class for validating PM record types in 'retour' files.

    Provides validation methods specific to the PM record type in 'retour' file format.
    """
    def __init__(self):
        """Initialize PM Retour validator with any necessary configuration."""
        pass
    
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
        # Create an instance of PMValidation to use its methods
        pm_validator = PMValidation()
        # Use the existing PMValidation method or implement custom validation
        pm_validator.validate_pm_structure(
            fields, row_number, validators, error_collector
        )


class P20RetourValidation:
    """
    Class for validating P_20 record types in 'retour' files.

    Provides validation methods specific to the P_20 record type in 'retour' file format.
    """
    def __init__(self):
        """Initialize P20 Retour validator with any necessary configuration."""
        pass
    
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
        # Create an instance of P20Validation to use its methods
        p20_validator = P20Validation()
        # Use the existing P20Validation method or implement custom validation
        p20_validator.validate_p_20_structure(
            fields, row_number, validators, error_collector
        )
