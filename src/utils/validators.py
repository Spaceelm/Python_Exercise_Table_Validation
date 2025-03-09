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
        - Column with index 100 should contain a date in format yyyymmddhhmmss (in reference file)
        - Column with index 101 should be empty for "ouverte" addresses, or contain a date for "ferme" addresses
        - Column 25 determines if the address is "fiscale" or "courier"
        - For "fiscale" addresses: Column 87 should have value 2 to be considered "ouverte"
        - For "courier" addresses: Column 87 should have value 1 to be considered "ouverte"
        
        The validation determines if an address is "ouverte" (valid) or "ferme" (closed) based on:
        - "Ouverte": Column 101 is empty and type-specific conditions for column 87 are met
        - "Ferme": Column 101 contains a date (closing date of the address)
        
        Args:
            fields: List of field values from the row
            row_number: Row number for error reporting
            reference_file_path: Path to the GD_Adresse_IP.csv file
            error_collector: Optional ErrorCollector instance to collect validation errors
            
        Returns:
            bool: True if validation passes, False otherwise
        """
        # Extract the PM ID from the P_20 record
        p20_pm_id = fields[1] if len(fields) > 1 else None
        if not p20_pm_id:
            if error_collector:
                error_collector.add_error(
                    "content",
                    "reference",
                    "P_20",
                    "Missing PM ID in P_20 record",
                    row=row_number,
                )
            else:
                print(f"[P_20] Row {row_number}: Missing PM ID in P_20 record")
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
        
        # Initialize variables to store information from reference file
        is_valid = False
        address_status = "unknown"
        reference_date = None
        address_type = None
        validation_value = None
        
        try:
            with open(reference_file_path, 'r', encoding='utf-8') as ref_file:
                csv_reader = csv.reader(ref_file)
                for ref_row in csv_reader:
                    # Look for the matching ID in the reference file
                    # Adjust this matching logic based on how IDs are stored in both files
                    if len(ref_row) > 0 and ref_row[0].strip() == p20_pm_id:
                        # 1. Check if column 100 has a date (reference file)
                        date_column_index = 100
                        has_date = False
                        if len(ref_row) > date_column_index and ref_row[date_column_index].strip() != '':
                            try:
                                # Format is yyyymmddhhmmss
                                reference_date = ref_row[date_column_index].strip()
                                datetime.strptime(reference_date, "%Y%m%d%H%M%S")
                                has_date = True
                            except (ValueError, IndexError):
                                has_date = False
                        
                        # 2. Check if column 101 is empty (for "ouverte" status)
                        closing_date_index = 101
                        is_column_101_empty = len(ref_row) <= closing_date_index or ref_row[closing_date_index].strip() == ''
                        
                        # 3. Determine address type from column 25
                        address_type_index = 25
                        address_type = "unknown"
                        if len(ref_row) > address_type_index:
                            address_type_value = ref_row[address_type_index].strip()
                            if address_type_value == '1':
                                address_type = "courier"
                            else:
                                address_type = "fiscale"
                        
                        # 4. Check column 87 value based on address type
                        address_validation_index = 87
                        has_valid_validation_value = False
                        validation_value = None
                        
                        if len(ref_row) > address_validation_index:
                            validation_value = ref_row[address_validation_index].strip()
                            
                            if address_type == "fiscale":
                                # For fiscale addresses, column 87 should be 2
                                has_valid_validation_value = validation_value == '2'
                            elif address_type == "courier":
                                # For courier addresses, column 87 should be 1
                                has_valid_validation_value = validation_value == '1'
                        
                        # Determine address status
                        if is_column_101_empty:
                            address_status = "ouverte"
                        else:
                            address_status = "ferme"
                            
                        # Set validity based on conditions
                        # For "ouverte" addresses: date exists, column 101 is empty, appropriate column 87 value
                        if has_date and is_column_101_empty and has_valid_validation_value:
                            is_valid = True
                        
                        break  # Found matching record, stop searching
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
        
        # Store the current row for order validation
        # Use the date from the reference file
        self.pm_to_p20_mapping[p20_pm_id].append({
            'row_number': row_number,
            'date': reference_date,
            'fields': fields,
            'status': address_status,
            'address_type': address_type,
            'validation_value': validation_value
        })
        
        if not is_valid:
            error_message = f"P_20 record does not meet validation criteria. Status: {address_status}, Type: {address_type}"
            if error_collector:
                error_collector.add_error(
                    "content",
                    "reference",
                    "P_20",
                    error_message,
                    row=row_number,
                )
            else:
                print(f"[P_20] Row {row_number}: {error_message}")
        
        return is_valid
        
    def validate_p20_ordering(
            self,
            error_collector: Optional[ErrorCollector] = None,
    ) -> bool:
        """
        Validate that P_20 records for each PM are ordered by date.
        
        This method checks that "ouverte" P_20 addresses are ordered by date (yyyymmddhhmmss)
        from the reference file. The date information is stored in column 100 of the reference file.
        
        Args:
            error_collector: Optional ErrorCollector instance to collect validation errors
            
        Returns:
            bool: True if all P_20 records are properly ordered, False otherwise
        """
        overall_valid = True
        
        for pm_id, p20_records in self.pm_to_p20_mapping.items():
            # Only validate ordering for "ouverte" addresses
            ouverte_records = [rec for rec in p20_records if rec.get('status') == 'ouverte']
            
            if not ouverte_records:
                continue
                
            # Sort records by date
            sorted_records = sorted(
                ouverte_records, 
                key=lambda x: x.get('date', '') if x.get('date') else ''
            )
            
            # Check if the current order matches the sorted order
            is_ordered = sorted_records == ouverte_records
            
            if not is_ordered:
                overall_valid = False
                
                # Find the first out-of-order record
                for i, rec in enumerate(ouverte_records):
                    if i > 0 and rec != sorted_records[i]:
                        error_message = f"P_20 records for PM {pm_id} are not ordered by date. Row {rec['row_number']} is out of order."
                        
                        if error_collector:
                            error_collector.add_error(
                                "content", 
                                "ordering", 
                                "P_20", 
                                error_message
                            )
                        else:
                            print(f"[P_20] {error_message}")
                        break
        
        return overall_valid
        
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
