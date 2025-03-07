"""
Validator classes for CSV data validation.

This module provides validator classes for different types of CSV records (PM, P_20, PM_10).
These classes define validation methods for each field in the records.
"""
import re
from datetime import datetime
from typing import Optional, List, Callable, Dict
import csv
import os

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
        self.pm_to_p20_mapping = {}  # Dictionary to track PM and associated P_20 records
        self.current_pm_id = None  # Track the current PM ID for associating P_20 records
    
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
        
    def validate_gd_adresse_ip_reference(
            self,
            fields: List[str],
            row_number: int,
            reference_file_path: str = "data/GD_Adresse_IP.csv",
            error_collector: Optional[ErrorCollector] = None,
    ) -> bool:
        """
        Validate P_20 records against reference data in GD_Adresse_IP.csv.
        
        Validates that P_20 values are valid according to conditions in GD_Adresse_IP.csv:
        - Column A should be filled with a date
        - Column B should be empty
        - Column C should equal to int 2
        
        Args:
            fields: List of field values from the row
            row_number: Row number for error reporting
            reference_file_path: Path to the GD_Adresse_IP.csv file
            error_collector: Optional ErrorCollector instance to collect validation errors
            
        Returns:
            bool: True if validation passes, False otherwise
        """
        # Get the ID from the P_20 record (assuming column 2 has the ID that links to PM)
        p20_pm_id = fields[1] if len(fields) > 1 else None
        
        # Skip validation if no ID is available
        if not p20_pm_id:
            if error_collector:
                error_collector.add_error(
                    "content",
                    "reference",
                    "P_20",
                    f"Missing PM ID reference in P_20 record",
                    row=row_number,
                )
            else:
                print(
                    f"[P_20] Row {row_number}: Missing PM ID reference in P_20 record"
                )
            return False
            
        # Check if reference file exists
        if not os.path.exists(reference_file_path):
            if error_collector:
                error_collector.add_error(
                    "content",
                    "reference",
                    "P_20",
                    f"Reference file {reference_file_path} not found",
                    row=row_number,
                )
            else:
                print(
                    f"[P_20] Row {row_number}: Reference file {reference_file_path} not found"
                )
            return False
            
        # Track this P_20 record under its PM ID for order validation later
        if p20_pm_id not in self.pm_to_p20_mapping:
            self.pm_to_p20_mapping[p20_pm_id] = []
        
        # Store the current row for order validation
        # Assuming the date information is in one of the P_20 fields
        # Adjust the index as needed to match the actual date field in your P_20 record
        date_field_index = 3  # Example index, adjust based on actual data
        date_value = fields[date_field_index] if len(fields) > date_field_index else None
        
        self.pm_to_p20_mapping[p20_pm_id].append({
            'row_number': row_number,
            'date': date_value,
            'fields': fields
        })
        
        # Validate against reference data
        is_valid = False
        try:
            with open(reference_file_path, 'r', encoding='utf-8') as ref_file:
                csv_reader = csv.reader(ref_file)
                for ref_row in csv_reader:
                    # Check the validation conditions
                    # 1. Column A should be filled with a date
                    has_date_in_column_a = ref_row[0].strip() != ''
                    try:
                        # Try to parse the date to ensure it's valid
                        datetime.strptime(ref_row[0], "%Y-%m-%d")  # Adjust format as needed
                    except (ValueError, IndexError):
                        has_date_in_column_a = False
                    
                    # 2. Column B should be empty
                    is_column_b_empty = len(ref_row) <= 1 or ref_row[1].strip() == ''
                    
                    # 3. Column C should equal to int 2
                    is_column_c_int_2 = False
                    if len(ref_row) > 2:
                        try:
                            is_column_c_int_2 = int(ref_row[2].strip()) == 2
                        except (ValueError, IndexError):
                            is_column_c_int_2 = False
                    
                    # If all conditions are met, the record is valid
                    if has_date_in_column_a and is_column_b_empty and is_column_c_int_2:
                        is_valid = True
                        break
        except Exception as e:
            if error_collector:
                error_collector.add_error(
                    "content",
                    "reference",
                    "P_20",
                    f"Error validating against reference: {str(e)}",
                    row=row_number,
                )
            else:
                print(
                    f"[P_20] Row {row_number}: Error validating against reference: {str(e)}"
                )
            return False
        
        if not is_valid:
            if error_collector:
                error_collector.add_error(
                    "content",
                    "reference",
                    "P_20",
                    f"P_20 record does not match reference data criteria in {reference_file_path}",
                    row=row_number,
                )
            else:
                print(
                    f"[P_20] Row {row_number}: P_20 record does not match reference data criteria in {reference_file_path}"
                )
        
        return is_valid
        
    def validate_p20_ordering(
            self,
            error_collector: Optional[ErrorCollector] = None,
    ) -> bool:
        """
        Validate that P_20 records for each PM are ordered by date.
        
        This method should be called after all P_20 records have been processed
        to check the ordering of P_20 records under each PM.
        
        Args:
            error_collector: Optional ErrorCollector instance to collect validation errors
            
        Returns:
            bool: True if all P_20 records are properly ordered, False otherwise
        """
        all_valid = True
        
        for pm_id, p20_records in self.pm_to_p20_mapping.items():
            if len(p20_records) <= 1:
                continue  # No ordering to check if only one record
                
            # Sort the records by date
            try:
                # Convert string dates to datetime objects for proper comparison
                for record in p20_records:
                    if record['date']:
                        try:
                            # Adjust the date format as needed
                            record['datetime'] = datetime.strptime(record['date'], "%Y-%m-%d")
                        except ValueError:
                            record['datetime'] = None
                    else:
                        record['datetime'] = None
                
                # Sort records by date
                sorted_records = sorted(
                    [r for r in p20_records if r['datetime'] is not None],
                    key=lambda x: x['datetime']
                )
                
                # Check if the original order matches the sorted order
                original_order = [r['row_number'] for r in p20_records if r['datetime'] is not None]
                sorted_order = [r['row_number'] for r in sorted_records]
                
                if original_order != sorted_order:
                    all_valid = False
                    if error_collector:
                        error_collector.add_error(
                            "content",
                            "ordering",
                            "P_20",
                            f"P_20 records for PM ID {pm_id} are not ordered by date",
                            row=sorted_order[0],  # Report on the first record
                        )
                    else:
                        print(
                            f"[P_20] P_20 records for PM ID {pm_id} are not ordered by date. "
                            f"Expected order: {sorted_order}, Actual order: {original_order}"
                        )
            except Exception as e:
                all_valid = False
                if error_collector:
                    error_collector.add_error(
                        "content",
                        "ordering",
                        "P_20",
                        f"Error checking P_20 record ordering for PM ID {pm_id}: {str(e)}",
                        row=p20_records[0]['row_number'] if p20_records else 0,
                    )
                else:
                    print(
                        f"[P_20] Error checking P_20 record ordering for PM ID {pm_id}: {str(e)}"
                    )
        
        return all_valid
        
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
