"""
Module for CSV content validation.

This module provides functionality for validating the content of CSV files,
focusing on the validation of individual data fields and row structures.
"""
import csv
from typing import List, Callable, Any, Optional

from future.backports.datetime import datetime


def validate_code_pays_insee_iso2(country_code: str) -> bool:
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
    with open("data/v_pays_territoire_2024.csv", encoding="utf8") as insee_file:
        insee_reader = csv.reader(insee_file)
        insee_header = next(insee_reader)
        if not insee_header:
            print("Error found in header. Content is empty")
            return False

        for insee_row in insee_reader:
            if insee_row[6].strip() == country_code:
                return True
        return False


class ContentValidation:
    """
    Class for validating CSV file content.
    
    This class provides methods and nested classes for validating the actual content
    of CSV files, excluding header and footer sections. It includes specialized
    validation for different record types (PM, PM_10, P_20).
    """

    class PM10Validation:
        """
        Class for validating PM_10 type records.
        
        Provides methods for validating the structure and field content
        of PM_10 type records in CSV files.
        """

        @staticmethod
        def validate_column5_code_ape(field: str) -> bool:
            """
            Validate the code APE field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 128), False otherwise
                
            Note:
                This field is optional but must be 128 characters or less when present.
            """
            return len(field) <= 128

        @staticmethod
        def validate_pm_10_structure(
            fields: List[str], 
            row_number: int, 
            validators_pm10: List[Callable[[str], bool]]
        ) -> None:
            """
            Validate PM_10 record structure and field formats.
            
            Args:
                fields: List of field values from the row
                row_number: Row number for error reporting
                validators_pm10: List of validator functions to apply
                
            Returns:
                None. Validation errors are printed to console.
            """
            # Proceed checking the number of columns
            if len(fields) != 5:
                print(
                    f"Row {row_number}: "
                    f"Invalid number of columns: {len(fields)} (expected 5)"
                )
            # Validate each field
            for i, (validator, field_tuple) in enumerate(zip(validators_pm10, fields)):
                if not validator(field_tuple):
                    print(
                        f"[PM_10] Row {row_number}, "
                        f"Column{i + 1}: "
                        f"Invalid value '{field_tuple}'. "
                        f"Validate rules for column"
                    )

        @staticmethod
        def validate_pm_10_structure_with_collector(
            fields: List[str], 
            row_number: int, 
            validators_pm10: List[Callable[[str], bool]],
            error_collector: Any
        ) -> None:
            """
            Validate PM_10 record structure and field formats using error collector.
            
            Args:
                fields: List of field values from the row
                row_number: Row number for error reporting
                validators_pm10: List of validator functions to apply
                error_collector: ErrorCollector instance to collect validation errors
                
            Returns:
                None. Validation errors are added to the error collector.
            """
            # Proceed checking the number of columns
            if len(fields) != 5:
                error_collector.add_error(
                    'content', 
                    'structure', 
                    'PM_10',
                    f"Invalid number of columns: {len(fields)} (expected 5)",
                    row=row_number
                )
            
            # Validate each field
            for i, (validator, field_tuple) in enumerate(zip(validators_pm10, fields)):
                if not validator(field_tuple):
                    error_collector.add_error(
                        'content', 
                        'format', 
                        f'PM_10_Column{i + 1}',
                        f"Invalid value '{field_tuple}'. Validate rules for column",
                        row=row_number
                    )

    class P20Validation:
        """
        Class for validating P_20 type records.
        
        Provides methods for validating the structure and field content
        of P_20 type records in CSV files.
        """

        @staticmethod
        def validate_column5_l1_address(field: str) -> bool:
            """
            Validate the L1 address field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 128), False otherwise
                
            Note:
                This field is optional but must be 128 characters or less when present.
            """
            return len(field) <= 128

        @staticmethod
        def validate_column6_l2_address(field: str) -> bool:
            """
            Validate the L2 address field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 128), False otherwise
                
            Note:
                This field is optional but must be 128 characters or less when present.
            """
            return len(field) <= 128

        @staticmethod
        def validate_column7_l3_address(field: str) -> bool:
            """
            Validate the L3 address field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 128), False otherwise
                
            Note:
                This field is optional but must be 128 characters or less when present.
            """
            return len(field) <= 128

        @staticmethod
        def validate_column8_l4_address(field: str) -> bool:
            """
            Validate the L4 address field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 128), False otherwise
                
            Note:
                This field is optional but must be 128 characters or less when present.
            """
            return len(field) <= 128

        @staticmethod
        def validate_column9_l5_adresse(field: str) -> bool:
            """
            Validate the L5 address field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 128), False otherwise
                
            Note:
                This field is optional but must be 128 characters or less when present.
            """
            return len(field) <= 128

        @staticmethod
        def validate_column10_l6_adresse(field: str) -> bool:
            """
            Validate the L6 address field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 128), False otherwise
                
            Note:
                This field is optional but must be 128 characters or less when present.
            """
            return len(field) <= 128

        @staticmethod
        def validate_column11_code_postal(field: str) -> bool:
            """
            Validate the postal code field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 128), False otherwise
                
            Note:
                This field is optional but must be 128 characters or less when present.
            """
            return len(field) <= 128

        @staticmethod
        def validate_column12_commune(field: str) -> bool:
            """
            Validate the commune field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 128), False otherwise
                
            Note:
                This field is optional but must be 128 characters or less when present.
            """
            return len(field) <= 128

        @staticmethod
        def validate_column13_state(field: str) -> bool:
            """
            Validate the state field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 10), False otherwise
                
            Note:
                This field is optional but must be 10 characters or less when present.
            """
            return len(field) <= 10

        @staticmethod
        def validate_column14_pays(field: str) -> bool:
            """
            Validate the country field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 128 and valid ISO2 code), False otherwise
                
            Note:
                This field is optional but must be 128 characters or less and a valid ISO2 code when present.
            """
            return len(field) <= 128 and validate_code_pays_insee_iso2(field)

        @staticmethod
        def validate_p_20_structure(
            fields: List[str], 
            row_number: int, 
            validators_p20: List[Callable[[str], bool]]
        ) -> None:
            """
            Validate P_20 record structure and field formats.
            
            Args:
                fields: List of field values from the row
                row_number: Row number for error reporting
                validators_p20: List of validator functions to apply
                
            Returns:
                None. Validation errors are printed to console.
            """
            # Proceed checking the number of columns
            if len(fields) != 14:
                print(
                    f"Row {row_number}: "
                    f"Invalid number of columns: {len(fields)} (expected 14)"
                )
            # Validate each field
            for i, (validator, field) in enumerate(zip(validators_p20, fields)):
                if not validator(field):
                    print(
                        f"[P_20] Row {row_number}, "
                        f"Column{i + 1}: Invalid value '{field}'. "
                        f"Validate rules for column"
                    )

        @staticmethod
        def validate_p_20_structure_with_collector(
            fields: List[str], 
            row_number: int, 
            validators_p20: List[Callable[[str], bool]],
            error_collector: Any
        ) -> None:
            """
            Validate P_20 record structure and field formats using error collector.
            
            Args:
                fields: List of field values from the row
                row_number: Row number for error reporting
                validators_p20: List of validator functions to apply
                error_collector: ErrorCollector instance to collect validation errors
                
            Returns:
                None. Validation errors are added to the error collector.
            """
            # Check the number of columns (assuming 14 for P_20)
            expected_columns = 14
            if len(fields) != expected_columns:
                error_collector.add_error(
                    'content', 
                    'structure', 
                    'P_20',
                    f"Invalid number of columns: {len(fields)} (expected {expected_columns})",
                    row=row_number
                )
            
            # Validate each field
            for i, (validator, field) in enumerate(zip(validators_p20, fields)):
                if not validator(field):
                    error_collector.add_error(
                        'content', 
                        'format', 
                        f'P_20_Column{i + 1}',
                        f"Invalid value '{field}'. Validate rules for column",
                        row=row_number
                    )

    class PMValidation:
        """
        Class for validating PM type records.
        
        Provides methods for validating the structure and field content
        of PM type records in CSV files.
        """

        @staticmethod
        def validate_column1_type_enregistrement(field: str) -> bool:
            """
            Validate the registration type field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (one of 'PM', 'P_20', 'PM_10'), False otherwise
                
            Note:
                This field must be one of 'PM', 'P_20', or 'PM_10'.
            """
            return (field == "PM") or (field == "P_20") or (field == "PM_10")

        @staticmethod
        def validate_column2_id_stable(field: str) -> bool:
            """
            Validate the stable ID field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 128 and alphanumeric), False otherwise
                
            Note:
                This field must be 128 characters or less and alphanumeric.
            """
            return len(field) <= 128 and field.isalnum()

        @staticmethod
        def validate_column3_uuid(field: str) -> bool:
            """
            Validate the UUID field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (alphanumeric), False otherwise
                
            Note:
                This field must be alphanumeric.
            """
            return field.isalnum()

        @staticmethod
        def validate_column4_network(field: str) -> bool:
            """
            Validate the network field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 32 and alphanumeric with spaces), False otherwise
                
            Note:
                This field must be 32 characters or less and alphanumeric with spaces.
            """
            return len(field) <= 32 and all(
                character.isalnum() or character.isspace() for character in field
            )

        @staticmethod
        def validate_column5_denomination_social(field: str) -> bool:
            """
            Validate the social denomination field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 250), False otherwise
                
            Note:
                This field must be 250 characters or less.
            """
            return len(field) <= 250

        @staticmethod
        def validate_column6_siren(field: str) -> bool:
            """
            Validate the SIREN field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 18), False otherwise
                
            Note:
                This field must be 18 characters or less.
            """
            return len(field) <= 18

        @staticmethod
        def validate_column7_siret(field: str) -> bool:
            """
            Validate the SIRET field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 18), False otherwise
                
            Note:
                This field must be 18 characters or less.
            """
            return len(field) <= 18

        @staticmethod
        def validate_column8_type_other_immatriculation(field: str) -> bool:
            """
            Validate the other registration type field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 18), False otherwise
                
            Note:
                This field must be 18 characters or less.
            """
            return len(field) <= 18

        @staticmethod
        def validate_column9_autre_immatriculation(field: str) -> bool:
            """
            Validate the other registration field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 128), False otherwise
                
            Note:
                This field must be 128 characters or less.
            """
            return len(field) <= 128

        @staticmethod
        def validate_column10_identifiant_rna(field: str) -> bool:
            """
            Validate the RNA identifier field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 10), False otherwise
                
            Note:
                This field must be 10 characters or less.
            """
            return len(field) <= 10

        @staticmethod
        def validate_column11_autre_numero_association(field: str) -> bool:
            """
            Validate the other association number field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 128), False otherwise
                
            Note:
                This field must be 128 characters or less.
            """
            return len(field) <= 128

        @staticmethod
        def validate_column12_code_categorie_juridique(field: str) -> bool:
            """
            Validate the legal category code field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 128), False otherwise
                
            Note:
                This field must be 128 characters or less.
            """
            return len(field) <= 128

        @staticmethod
        def validate_column13_code_pays_enregistrement(field: str) -> bool:
            """
            Validate the registration country code field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 128 and valid ISO2 code), False otherwise
                
            Note:
                This field must be 128 characters or less and a valid ISO2 code.
            """
            return len(field) <= 128 and validate_code_pays_insee_iso2(field)

        @staticmethod
        def validate_column14_resultat_verification(field: str) -> bool:
            """
            Validate the verification result field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (length <= 128), False otherwise
                
            Note:
                This field must be 128 characters or less.
            """
            return len(field) <= 128

        @staticmethod
        def validate_column15_date_derniere_verification(field: str) -> bool:
            """
            Validate the last verification date field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (format 'yyyymmddhhmmss'), False otherwise
                
            Note:
                This field must be in the format 'yyyymmddhhmmss'.
            """
            if len(field) != 0:
                try:
                    datetime.strptime(field, "%Y%m%d%H%M%S")
                    return True
                except ValueError:
                    return False
            elif len(field) == 0:
                return True

        @staticmethod
        def validate_column16_date_evolution_pm_chez_cardif(field: str) -> bool:
            """
            Validate the PM evolution date at Cardif field.
            
            Args:
                field: The field value to validate
                
            Returns:
                bool: True if validation passes (format 'yyyymmddhhmmss'), False otherwise
                
            Note:
                This field must be in the format 'yyyymmddhhmmss'.
            """
            if len(field) != 0:
                try:
                    datetime.strptime(field, "%Y%m%d%H%M%S")
                    return True
                except ValueError:
                    return False
            elif len(field) == 0:
                return True

        @staticmethod
        def validate_pm_structure(
            fields: List[str], 
            row_number: int, 
            validators_pm: List[Callable[[str], bool]]
        ) -> None:
            """
            Validate PM record structure and field formats.
            
            Args:
                fields: List of field values from the row
                row_number: Row number for error reporting
                validators_pm: List of validator functions to apply
                
            Returns:
                None. Validation errors are printed to console.
            """
            if len(fields) != 16:
                print(
                    f"Row {row_number}: Invalid number of columns: {len(fields)} (expected 16)"
                )
            # Validate each field
            for i, (validator, field) in enumerate(zip(validators_pm, fields)):

                if not validator(field):
                    print(
                        f"[PM] Row {row_number}, Column{i + 1}: Invalid value '{field}'. Validate rules for column"
                    )

        @staticmethod
        def validate_pm_structure_with_collector(
            fields: List[str], 
            row_number: int, 
            validators_pm: List[Callable[[str], bool]],
            error_collector: Any
        ) -> None:
            """
            Validate PM record structure and field formats using error collector.
            
            Args:
                fields: List of field values from the row
                row_number: Row number for error reporting
                validators_pm: List of validator functions to apply
                error_collector: ErrorCollector instance to collect validation errors
                
            Returns:
                None. Validation errors are added to the error collector.
            """
            # Check the number of columns (assuming 16 for PM)
            expected_columns = 16
            if len(fields) != expected_columns:
                error_collector.add_error(
                    'content', 
                    'structure', 
                    'PM',
                    f"Invalid number of columns: {len(fields)} (expected {expected_columns})",
                    row=row_number
                )
            
            # Validate each field
            for i, (validator, field) in enumerate(zip(validators_pm, fields)):
                if not validator(field):
                    error_collector.add_error(
                        'content', 
                        'format', 
                        f'PM_Column{i + 1}',
                        f"Invalid value '{field}'. Validate rules for column",
                        row=row_number
                    )
