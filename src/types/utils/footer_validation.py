"""
Module for CSV footer validation.

This module provides functionality for validating the structure and content
of CSV file footers, which typically include summary information like
total row count.
"""
from src.utils.terminal_colors import TerminalColors


class FooterValidation:
    """
    Class for validating CSV file footers.
    
    This class provides methods for validating both the structure
    and individual field contents of CSV file footers.
    """

    @staticmethod
    def validate_column1_pied_type_enregistrement(field):
        """
        Validates that the footer type field has value 99.
        
        Args:
            field: The field value to validate
            
        Returns:
            bool: True if validation passes (value is 99), False otherwise
            
        Note:
            This field is mandatory and must have the value 99 to indicate a footer record.
        """
        result = field == 99
        if result:
            print(TerminalColors.success(f"Footer type validation: {TerminalColors.highlight_value(field)} is valid"))
        else:
            print(TerminalColors.error(f"Footer type validation: {TerminalColors.highlight_value(field)} is invalid (expected 99)"))
        return result

    @staticmethod
    def validate_column2_pied_nombre_lignes_du_fichier(field, line_num):
        """
        Validates the line count in the footer against actual file line count.
        
        Args:
            field (int): The line count value from the footer
            line_num (int): The actual number of lines in the file
            
        Returns:
            bool: True if the footer line count matches actual count (minus header and footer),
                 False otherwise
                 
        Note:
            The line count should equal the actual number of lines minus 2
            (to account for header and footer rows).
        """
        # Subtract 2 from line_num to exclude header and footer rows
        expected = line_num - 2
        result = expected == field
        
        if result:
            print(TerminalColors.success(f"Line count validation: {TerminalColors.highlight_value(field)} matches expected count ({expected})"))
        else:
            print(TerminalColors.error(f"Line count validation: {TerminalColors.highlight_value(field)} does not match expected count ({expected})"))
        return result

    @staticmethod
    def validate_footer_structure(reader, fields, row_number):
        """
        Validates the structure and position of the footer in the CSV file.
        
        Args:
            reader: CSV reader object
            fields: List of field values from the current row
            row_number: Row number for error reporting
            
        Returns:
            None. Validation results are printed to console.
            
        Note:
            This method checks if the current row is actually the last row in the file
            and performs footer-specific validations if it is.
        """
        # Inform that we're processing a potential footer row
        print(TerminalColors.processing(f"Checking potential footer in row: {TerminalColors.highlight_value(row_number)}..."))
        
        try:
            # Try to read the next line - if successful, this means the current row is not the footer
            final_line = next(reader)
            print(TerminalColors.warning(f"Line is not footer. Next line found: {TerminalColors.highlight_value(str(final_line))}."))
            print(TerminalColors.error("Type 99 should only be visible in final line."))
        except StopIteration:
            # If StopIteration is raised, we've reached the end of the file, confirming this is the footer
            print(TerminalColors.section_header("VALIDATING FOOTER"))
            
            # Validate that the first field indicates a footer record (value 99)
            print(TerminalColors.processing("Validating footer type..."))
            FooterValidation.validate_column1_pied_type_enregistrement(fields[0])
            
            # Validate that the second field contains the correct line count
            print(TerminalColors.processing("Validating line count..."))
            # Get the total number of lines from the reader
            line_number = reader.line_num
            # Compare with the value in the footer
            FooterValidation.validate_column2_pied_nombre_lignes_du_fichier(
                fields[1], line_number
            )
            
            # Footer validation complete
            print(TerminalColors.section_end())
