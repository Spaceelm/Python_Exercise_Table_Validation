"""
Example script for validating a 'retour' format CSV file.

This script shows how to use the validation system with a 'retour' format file
by passing the appropriate command-line arguments to the main module.
"""
import sys
import os
import subprocess
from pathlib import Path

# Add the parent directory to sys.path to import modules from the parent directory
sys.path.append(str(Path(__file__).parent.parent))

def validate_retour_file(file_path, output_format='terminal'):
    """
    Validate a 'retour' format CSV file.
    
    Args:
        file_path: Path to the CSV file to validate
        output_format: Output format for validation results (terminal, html, json, or all)
        
    Returns:
        int: Return code from the validation process (0 for success)
    """
    # Convert the relative path to absolute path if necessary
    abs_file_path = os.path.abspath(file_path)
    
    # Check if the file exists
    if not os.path.exists(abs_file_path):
        print(f"Error: File '{abs_file_path}' not found.")
        return 1
    
    # Construct the command to run the main module with the specified arguments
    cmd = [
        sys.executable,
        os.path.join(Path(__file__).parent.parent, "main.py"),
        "--file", abs_file_path,
        "--file-type", "retour",
        "--format", output_format
    ]
    
    # Run the command and return the result
    result = subprocess.run(cmd)
    return result.returncode

if __name__ == "__main__":
    # Parse command-line arguments
    if len(sys.argv) < 2:
        print("Usage: python validate_retour_file.py <file_path> [output_format]")
        sys.exit(1)
        
    file_path = sys.argv[1]
    output_format = sys.argv[2] if len(sys.argv) > 2 else 'terminal'
    
    # Validate the file
    result = validate_retour_file(file_path, output_format)
    sys.exit(result)
