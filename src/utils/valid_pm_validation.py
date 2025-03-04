"""
Module for PM (Personne Morale) validation.

This module provides functionality for validating the structure 
and correctness of PM data through extraction and comparison.
"""
import csv  # Import CSV module for file operations
from src.utils.terminal_colors import TerminalColors
from src.utils.tqdm_config import custom_bar_format  # Import the custom bar format
from typing import Dict, List, Iterator
from tqdm import tqdm  # Import tqdm for progress bars


class ValidPmValidation:
    """
    Class for validation of PM (Personne Morale) content.
    
    This class provides methods for importing and validating PM data
    by comparing it against reference data.
    """

    @staticmethod
    def import_pm_table(reader_aller_file: Iterator[List[str]]) -> None:
        """
        Import files and validate PM content through comparison.
        
        Args:
            reader_aller_file: CSV reader object containing the 'aller' file data
            
        Returns:
            None. Results are printed to console during processing.
            
        Note:
            This method compares data from 'exported_pm_id.csv' and 'filtered_csv.csv'
            against the provided reader_aller_file to validate PM content.
        """
        # Read and process exported PM IDs
        with open("data/exported_pm_id.csv", encoding="utf8") as file:
            # Create a reader that filters out null bytes (\0) which can cause parsing issues
            reader = csv.reader((row.replace("\0", "") for row in file))
            # Read the header row
            header: List[str] = next(reader)
            print(TerminalColors.info(f"Header: {TerminalColors.highlight_value(','.join(header))}"))
            
            print(TerminalColors.processing("Filtering and preparing reference data..."))
            with open("data/filtered_csv.csv", "w", encoding="utf8") as new:
                new_csv = csv.writer(new, delimiter=",", lineterminator="\n")
                ok_count: int = 0
                for pm_row in tqdm(reader, 
                                  desc="Filtering reference data", 
                                  unit="records",
                                  ncols=100,
                                  bar_format=custom_bar_format):
                    if pm_row[70] == "ACTIF" or pm_row[70] == "INACTIF":
                        ok_count += 1
                        new_csv.writerow(pm_row)
                print(TerminalColors.success(f"\nFiltering complete. {ok_count} lines processed."))
                
        with open("data/filtered_csv.csv", encoding="utf8") as filtered_file:
            # Open the pre-filtered CSV file
            filtered_csv_reader = csv.reader(filtered_file)
            
            # Initialize counters and dictionaries for tracking matches
            matches_count: int = 0          # Count of matches found
            non_matches_count: int = 0      # Count of non-matches
            pm_count: int = 0               # Count of PM records in aller file
            row_count_filtered_csv: int = 0 # Count of rows in filtered CSV
            
            # Dictionaries to store data for quick lookup
            aller_dict: Dict[str, List[str]] = {}                    # Dictionary of aller rows by ID
            filtered_dict: Dict[str, List[str]] = {}                 # Dictionary of filtered rows by ID
            aller_dict_for_inverted_check: Dict[str, List[str]] = {} # Copy for the inverted check
            
            # First pass: Process aller file data
            print(TerminalColors.processing("Reading PM records from input file..."))
            pm_count: int = 0
            pm_rows = []
            for aller_row in reader_aller_file:
                if aller_row[0] == "PM":
                    pm_rows.append(aller_row)
            
            for aller_row in tqdm(pm_rows, 
                                desc="Processing PM records", 
                                unit="records",
                                ncols=100,
                                bar_format=custom_bar_format):
                pm_count += 1
                # Store the row in dictionaries using the ID (second column) as key
                aller_dict[aller_row[1]] = aller_row
                aller_dict_for_inverted_check[aller_row[1]] = aller_row
            print(TerminalColors.success(f"Processed {pm_count} PM records."))
            
            # Second pass: Process filtered CSV data
            print(TerminalColors.processing("Loading reference data..."))
            for filtered_row in filtered_csv_reader:
                # Store filtered rows in dictionary using the ID (first column) as key
                filtered_dict[filtered_row[0]] = filtered_row

            # First comparison: filtered_dict → aller_dict
            # This checks if each ID in filtered_dict exists in aller_dict
            print(TerminalColors.processing("Starting validation - checking reference IDs against input file..."))
            for filtered_key in tqdm(filtered_dict, 
                                   desc="Forward validation", 
                                   unit="IDs",
                                   ncols=100,
                                   bar_format=custom_bar_format):
                row_count_filtered_csv += 1
                
                try:
                    # Try to find this key in the aller dictionary and remove it if found
                    aller_row = aller_dict.pop(filtered_key)
                    # Get the filtered row with the same ID
                    filtered_row = filtered_dict[aller_row[1]]
                    
                    # Validate that the IDs match
                    if filtered_row[0] == aller_row[1]:
                        matches_count += 1
                    else:
                        print(TerminalColors.error("ID match error"))
                except KeyError:
                    # If the key doesn't exist in aller_dict, count as non-match
                    non_matches_count += 1
            
            # Report unmatched rows from aller
            print("\n")
            for unmatched_key in aller_dict:
                print(
                    TerminalColors.warning(
                        f"PM in input file without match: {TerminalColors.highlight_value(str(aller_dict[unmatched_key]))}"
                    )
                )
            
            # Inverted comparison: aller_dict → filtered_dict
            # This checks if each ID in aller_dict exists in filtered_dict
            inverted_matches_count = 0
            inverted_non_matches_count = 0
            row_count_aller_csv = 0
            print("\n" + TerminalColors.processing("Starting reverse validation - checking input IDs against reference file..."))
            
            for aller_key in tqdm(aller_dict_for_inverted_check, 
                                desc="Reverse validation", 
                                unit="IDs",
                                ncols=100,
                                bar_format=custom_bar_format):
                row_count_aller_csv += 1
                
                try:
                    # Try to find this key in the filtered dictionary and remove it if found
                    filtered_row = filtered_dict.pop(aller_key)
                    # Get the aller row with the same ID
                    aller_row = aller_dict_for_inverted_check[filtered_row[0]]
                    
                    # Validate that the IDs match
                    if filtered_row[0] == aller_row[1]:
                        inverted_matches_count += 1
                    else:
                        print(TerminalColors.error("ID match error"))
                except KeyError:
                    # If the key doesn't exist in filtered_dict, count as non-match
                    inverted_non_matches_count += 1
                    
            # Print final validation summary
            print("\n" + TerminalColors.info(f"Validation Summary:"))
            print(TerminalColors.success(f"Forward matches: {str(matches_count)}/{str(row_count_filtered_csv)} ({(matches_count/row_count_filtered_csv*100 if row_count_filtered_csv else 0):.1f}%)"))
            print(TerminalColors.success(f"Reverse matches: {str(inverted_matches_count)}/{str(row_count_aller_csv)} ({(inverted_matches_count/row_count_aller_csv*100 if row_count_aller_csv else 0):.1f}%)"))
