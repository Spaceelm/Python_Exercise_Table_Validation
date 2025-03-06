"""
Type definitions and validator collections module.

This module defines validation lists for different record types (PM, P_20, PM_10)
in the validation system. It acts as a central repository for validator function
collections, ensuring consistent validation across the application.

Note:
    The order of functions in the validator lists is important and corresponds
    to the order of fields in the CSV file.
"""
# Import directly from validators.py to avoid circular imports
from src.utils.validators import (
    PMValidation,
    P20Validation,
    PM10Validation
)

# Initialize validators
pm_validator = PMValidation()
p20_validator = P20Validation()
pm10_validator = PM10Validation()
# List of validators for PM (Personne Morale) records
# Each validator corresponds to a specific column in the CSV file
validators_pm = [
    pm_validator.validate_column1_type_enregistrement,  # Validate record type (must be PM/P_20/PM_10)
    pm_validator.validate_column2_id_stable,  # Validate stable ID (length and alphanumeric)
    pm_validator.validate_column3_uuid,  # Validate UUID format (must be alphanumeric)
    pm_validator.validate_column4_network,  # Validate network code (length and character set)
    pm_validator.validate_column5_denomination_social,  # Validate company name (length <= 250)
    pm_validator.validate_column6_siren,  # Validate SIREN number (length <= 18)
    pm_validator.validate_column7_siret,  # Validate SIRET number (length <= 18)
    pm_validator.validate_column8_type_other_immatriculation,
    # Validate other registration type (length <= 18)
    pm_validator.validate_column9_autre_immatriculation,
    # Validate other registration number (length <= 128)
    pm_validator.validate_column10_identifiant_rna,  # Validate RNA identifier (length <= 10)
    pm_validator.validate_column11_autre_numero_association,
    # Validate other association number (length <= 128)
    pm_validator.validate_column12_code_categorie_juridique,
    # Validate legal category code (length <= 128)
    pm_validator.validate_column13_code_pays_enregistrement,  # Validate country code (ISO2 format)
    pm_validator.validate_column14_resultat_verification,
    # Validate verification result (length <= 128)
    pm_validator.validate_column15_date_derniere_verification,
    # Validate last verification date (format)
    pm_validator.validate_column16_date_evolution_pm_chez_cardif,
    # Validate PM evolution date (format)
]

# List of validators for P_20 (Address) records
# Each validator corresponds to a specific column in the CSV file
validators_p20 = [
    pm_validator.validate_column1_type_enregistrement,  # Validate record type (must be PM/P_20/PM_10)
    pm_validator.validate_column2_id_stable,  # Validate stable ID (length and alphanumeric)
    pm_validator.validate_column3_uuid,  # Validate UUID format (must be alphanumeric)
    pm_validator.validate_column4_network,  # Validate network code (length and character set)
    p20_validator.validate_column5_l1_address,  # Validate address line 1 (length <= 128)
    p20_validator.validate_column6_l2_address,  # Validate address line 2 (length <= 128)
    p20_validator.validate_column7_l3_address,  # Validate address line 3 (length <= 128)
    p20_validator.validate_column8_l4_address,  # Validate address line 4 (length <= 128)
    p20_validator.validate_column9_l5_adresse,  # Validate address line 5 (length <= 128)
    p20_validator.validate_column10_l6_adresse,  # Validate address line 6 (length <= 128)
    p20_validator.validate_column11_code_postal,  # Validate postal code (length <= 128)
    p20_validator.validate_column12_commune,  # Validate city/town (length <= 128)
    p20_validator.validate_column13_state,  # Validate state/province (length <= 10)
    p20_validator.validate_column14_pays,  # Validate country (ISO2 format)
]

# List of validators for PM_10 (Business Activity) records
# Each validator corresponds to a specific column in the CSV file
validators_pm10 = [
    pm_validator.validate_column1_type_enregistrement,  # Validate record type (must be PM/P_20/PM_10)
    pm_validator.validate_column2_id_stable,  # Validate stable ID (length and alphanumeric)
    pm_validator.validate_column3_uuid,  # Validate UUID format (must be alphanumeric)
    pm_validator.validate_column4_network,  # Validate network code (length and character set)
    pm10_validator.validate_column5_code_ape,  # Validate APE code (length <= 128)
]

# List of validators for "retour" file format records
# Each validator corresponds to a specific column in the "retour" file
validators_retour_pm = [
    pm_validator.validate_column1_type_enregistrement,  # Validate record type (must be PM/P_20/PM_10)
    pm_validator.validate_column2_id_stable,  # Validate stable ID (length and alphanumeric)
    pm_validator.validate_column3_uuid,  # Validate UUID format (must be alphanumeric)
    pm_validator.validate_column3_uuid,  # TODO add required validation for PMP ID
    pm_validator.validate_column3_uuid,  # TODO add required validation for ID
    pm_validator.validate_column4_network,  # Validate network code (length and character set)
    pm_validator.validate_column15_date_derniere_verification,  # TODO verify again
    pm_validator.validate_column14_resultat_verification,  # TODO needs validation with ok KO
    pm_validator.validate_column8_type_other_immatriculation,  # TODO needs to be 1 of 5
    pm_validator.validate_column6_siren,  # TODO score certitude to be added here
    pm_validator.validate_column6_siren,  # TODO nom entreprise added here
    pm_validator.validate_column5_denomination_social,  # Validate company name (length <= 250)
    pm_validator.validate_column5_denomination_social,  # TODO denomination comerciale added here
    pm_validator.validate_column5_denomination_social,  # TODO sigle added here
    pm_validator.validate_column5_denomination_social,  # TODO Enseigne added here
    pm_validator.validate_column6_siren,  # Validate SIREN number (length <= 18)
    pm_validator.validate_column7_siret,  # Validate SIRET number (length <= 18)
    pm_validator.validate_column8_type_other_immatriculation,
    # Validate other registration type (length <= 18)
    pm_validator.validate_column9_autre_immatriculation,
    pm_validator.validate_column5_denomination_social,  # TODO siret siege added here
    # Validate other registration number (length <= 128)
    pm_validator.validate_column10_identifiant_rna,  # Validate RNA identifier (length <= 10)
    pm_validator.validate_column11_autre_numero_association,
    # Validate other association number (length <= 128)
    pm_validator.validate_column5_denomination_social,  # TODO numero etablissement added here
    pm_validator.validate_column5_denomination_social,  # TODO statut entreprise added here
    pm_validator.validate_column5_denomination_social,  # TODO date maj code added here
    pm_validator.validate_column5_denomination_social,  # TODO judjement entreprise
    pm_validator.validate_column5_denomination_social,  # TODO etat etablissent
    pm_validator.validate_column5_denomination_social,  # TODO date creation
    pm_validator.validate_column5_denomination_social,  # TODO date enregistrement
    pm_validator.validate_column13_code_pays_enregistrement,  # Validate country code (ISO2 format)
    pm_validator.validate_column5_denomination_social,  # TODO ville enregistrement
    pm_validator.validate_column12_code_categorie_juridique,
    # Validate legal category code (length <= 128)
    pm_validator.validate_column14_resultat_verification,
    # Validate verification result (length <= 128)
    # Retour PM specific fields would be added/modified here as needed
]

validators_retour_p20 = [
    pm_validator.validate_column1_type_enregistrement,  # Validate record type (must be PM/P_20/PM_10)
    pm_validator.validate_column2_id_stable,  # Validate stable ID (length and alphanumeric)
    pm_validator.validate_column3_uuid,  # Validate UUID format (must be alphanumeric)
    pm_validator.validate_column4_network,  # Validate network code (length and character set)
    p20_validator.validate_column5_l1_address,  # Validate address line 1 (length <= 128)
    p20_validator.validate_column6_l2_address,  # Validate address line 2 (length <= 128)
    p20_validator.validate_column7_l3_address,  # Validate address line 3 (length <= 128)
    p20_validator.validate_column8_l4_address,  # Validate address line 4 (length <= 128)
    p20_validator.validate_column9_l5_adresse,  # Validate address line 5 (length <= 128)
    p20_validator.validate_column10_l6_adresse,  # Validate address line 6 (length <= 128)
    p20_validator.validate_column11_code_postal,  # Validate postal code (length <= 128)
    p20_validator.validate_column12_commune,  # Validate city/town (length <= 128)
    p20_validator.validate_column13_state,  # Validate state/province (length <= 10)
    # Retour P20 specific fields would be added/modified here as needed
]
