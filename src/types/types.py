"""
Type definitions and validator collections module.

This module defines validation lists for different record types (PM, P_20, PM_10)
in the validation system. It acts as a central repository for validator function
collections, ensuring consistent validation across the application.

Note:
    The order of functions in the validator lists is important and corresponds
    to the order of fields in the CSV file.
"""
from src.utils.content_validation import Content_validation  # Import validation functions

# List of validators for PM (Personne Morale) records
# Each validator corresponds to a specific column in the CSV file
validators_pm = [
    Content_validation.PM_validation.validate_column1_type_enregistrement,  # Validate record type (must be PM/P_20/PM_10)
    Content_validation.PM_validation.validate_column2_id_stable,  # Validate stable ID (length and alphanumeric)
    Content_validation.PM_validation.validate_column3_uuid,  # Validate UUID format (must be alphanumeric)
    Content_validation.PM_validation.validate_column4_network,  # Validate network code (length and character set)
    Content_validation.PM_validation.validate_column5_denomination_social,  # Validate company name (length <= 250)
    Content_validation.PM_validation.validate_column6_siren,  # Validate SIREN number (length <= 18)
    Content_validation.PM_validation.validate_column7_siret,  # Validate SIRET number (length <= 18)
    Content_validation.PM_validation.validate_column8_type_other_immatriculation,  # Validate other registration type (length <= 18)
    Content_validation.PM_validation.validate_column9_autre_immatriculation,  # Validate other registration number (length <= 128)
    Content_validation.PM_validation.validate_column10_identifiant_rna,  # Validate RNA identifier (length <= 10)
    Content_validation.PM_validation.validate_column11_autre_numero_association,  # Validate other association number (length <= 128)
    Content_validation.PM_validation.validate_column12_code_categorie_juridique,  # Validate legal category code (length <= 128)
    Content_validation.PM_validation.validate_column13_code_pays_enregistrement,  # Validate country code (ISO2 format)
    Content_validation.PM_validation.validate_column14_resultat_verification,  # Validate verification result (length <= 128)
    Content_validation.PM_validation.validate_column15_date_derniere_verification,  # Validate last verification date (format)
    Content_validation.PM_validation.validate_column16_date_evolution_pm_chez_cardif,  # Validate PM evolution date (format)
]

# List of validators for P_20 (Address) records
# Each validator corresponds to a specific column in the CSV file
validators_p20 = [
    Content_validation.PM_validation.validate_column1_type_enregistrement,  # Validate record type (must be PM/P_20/PM_10)
    Content_validation.PM_validation.validate_column2_id_stable,  # Validate stable ID (length and alphanumeric)
    Content_validation.PM_validation.validate_column3_uuid,  # Validate UUID format (must be alphanumeric)
    Content_validation.PM_validation.validate_column4_network,  # Validate network code (length and character set)
    Content_validation.P_20_validation.validate_column5_l1_address,  # Validate address line 1 (length <= 128)
    Content_validation.P_20_validation.validate_column6_l2_address,  # Validate address line 2 (length <= 128)
    Content_validation.P_20_validation.validate_column7_l3_address,  # Validate address line 3 (length <= 128)
    Content_validation.P_20_validation.validate_column8_l4_address,  # Validate address line 4 (length <= 128)
    Content_validation.P_20_validation.validate_column9_l5_adresse,  # Validate address line 5 (length <= 128)
    Content_validation.P_20_validation.validate_column10_l6_adresse,  # Validate address line 6 (length <= 128)
    Content_validation.P_20_validation.validate_column11_code_postal,  # Validate postal code (length <= 128)
    Content_validation.P_20_validation.validate_column12_commune,  # Validate city/town (length <= 128)
    Content_validation.P_20_validation.validate_column13_state,  # Validate state/province (length <= 10)
    Content_validation.P_20_validation.validate_column14_pays,  # Validate country (ISO2 format)
]

# List of validators for PM_10 (Business Activity) records
# Each validator corresponds to a specific column in the CSV file
validators_pm10 = [
    Content_validation.PM_validation.validate_column1_type_enregistrement,  # Validate record type (must be PM/P_20/PM_10)
    Content_validation.PM_validation.validate_column2_id_stable,  # Validate stable ID (length and alphanumeric)
    Content_validation.PM_validation.validate_column3_uuid,  # Validate UUID format (must be alphanumeric)
    Content_validation.PM_validation.validate_column4_network,  # Validate network code (length and character set)
    Content_validation.PM_10_validation.validate_column5_code_ape,  # Validate APE code (length <= 128)
]
