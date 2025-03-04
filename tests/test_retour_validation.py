"""
Test module for retour file validation.

This module tests the validation of 'retour' file format specifically
by creating sample data and verifying the validation rules.
"""
import unittest
from unittest.mock import patch, MagicMock
import csv
import io
from src.utils.retour_validation import RetourValidation
from src.utils.error_collector import ErrorCollector
from src.types.types import validators_retour_pm, validators_retour_p20


class TestRetourValidation(unittest.TestCase):
    """
    Test cases for 'retour' file format validation.
    
    These tests verify that the RetourValidation class correctly
    handles the validation of 'retour' file format with its specific
    column structure.
    """
    
    def setUp(self):
        """Set up test environment before each test."""
        self.error_collector = ErrorCollector()
        
        # Sample PM record for retour format
        self.sample_pm_record = [
            "PM",           # Record type
            "ID12345",      # Stable ID
            "UUID-XYZ",     # UUID
            "NETWORK",      # Network code
            "Company Name", # Denomination social
            "123456789",    # SIREN
            "12345678901234", # SIRET
            "TYPE",         # Type other immatriculation
            "AUTRE123",     # Autre immatriculation
            "RNA123456",    # Identifiant RNA
            "ASSOC123",     # Autre numéro association
            "1234",         # Code categorie juridique
            "FR",           # Code pays enregistrement
            "OK",           # Résultat vérification
            # Retour format might have fewer or different columns compared to aller
        ]
        
        # Sample P_20 record for retour format
        self.sample_p20_record = [
            "P_20",         # Record type
            "ID12345",      # Stable ID
            "UUID-XYZ",     # UUID
            "NETWORK",      # Network code
            "Address L1",   # L1 address
            "Address L2",   # L2 address
            "Address L3",   # L3 address
            "Address L4",   # L4 address
            "Address L5",   # L5 address
            "Address L6",   # L6 address
            "75000",        # Code postal
            "Paris",        # Commune
            "IDF",          # State
            # Retour format might have fewer or different columns compared to aller
        ]

    @patch('src.utils.content_validation.ContentValidation.PMValidation.validate_pm_structure')
    def test_pm_retour_validation(self, mock_validate_pm_structure):
        """
        Test the PM 'retour' validation.
        
        Verifies that the RetourValidation class correctly
        processes PM records in the 'retour' format.
        """
        # Call the RetourValidation method with sample data
        RetourValidation.PMRetourValidation.validate_pm_retour_structure(
            self.sample_pm_record, 1, validators_retour_pm, self.error_collector
        )
        
        # Verify that the underlying validation method was called with correct arguments
        mock_validate_pm_structure.assert_called_once_with(
            self.sample_pm_record, 1, validators_retour_pm, self.error_collector
        )
    
    @patch('src.utils.content_validation.ContentValidation.P20Validation.validate_p_20_structure')
    def test_p20_retour_validation(self, mock_validate_p20_structure):
        """
        Test the P_20 'retour' validation.
        
        Verifies that the RetourValidation class correctly
        processes P_20 records in the 'retour' format.
        """
        # Call the RetourValidation method with sample data
        RetourValidation.P20RetourValidation.validate_p20_retour_structure(
            self.sample_p20_record, 1, validators_retour_p20, self.error_collector
        )
        
        # Verify that the underlying validation method was called with correct arguments
        mock_validate_p20_structure.assert_called_once_with(
            self.sample_p20_record, 1, validators_retour_p20, self.error_collector
        )
    
    def test_column_retour_specific_field_validation(self):
        """
        Test the validation of retour-specific fields.
        
        Verifies that the specialized validation methods for
        retour-specific fields work correctly.
        """
        # Test with valid field
        valid_field = "ValidValue"
        self.assertTrue(
            RetourValidation.PMRetourValidation.validate_column_retour_specific_field(valid_field)
        )
        
        # Test with empty field
        empty_field = ""
        self.assertFalse(
            RetourValidation.PMRetourValidation.validate_column_retour_specific_field(empty_field)
        )
        
        # Test with None field
        none_field = None
        self.assertFalse(
            RetourValidation.PMRetourValidation.validate_column_retour_specific_field(none_field)
        )


if __name__ == '__main__':
    unittest.main()
