"""
Includes methods for initial setup of the project
"""
import argparse  # Import for command line argument parsing
from argparse import Namespace

from src.utils.error_collector import ErrorCollector
from src.utils.terminal_colors import TerminalColors


class Setup:
    """
    Class for collecting and organizing methods for initial setup of project
    """

    def __init__(self):
        """Initialize the setup"""
        # Main initialization point
        self.parser = argparse.ArgumentParser(description="CSV Table Validation Tool")
        self.encoding_to_utf8 = "utf8"
        self.aller_file_default_delimeter = "|"
        self.error_collector = ErrorCollector()

    def argument_parser(self) -> Namespace:
        """
        Method for including parser arguments
        """
        # Parse command line arguments
        self.parser.add_argument(
            "--file",
            type=str,
            default="data/20250203T210108.csv",
            help="Path to the CSV file to validate",
        )
        self.parser.add_argument(
            "--format",
            type=str,
            choices=["terminal", "html", "json", "all"],
            default="terminal",
            help="Output format for validation results",
        )
        self.parser.add_argument(
            "--file-type",
            type=str,
            choices=["aller", "retour"],
            default="aller",
            help="Type of file format (aller or retour)",
        )
        args = self.parser.parse_args()
        return args

    @staticmethod
    def line_counter(args):
        """
        line counter method
        """
        total_lines = sum(1 for _ in open(args.file, encoding="utf8"))

        print(
            TerminalColors.info(
                f"Processing file with {TerminalColors.highlight_value(str(total_lines))} lines"
            )
        )
        print(
            TerminalColors.info(
                f"File type: {TerminalColors.highlight_value(args.file_type)}"
            )
        )
        return total_lines

    @staticmethod
    def get_header(csv_reader):
        """
        method to get header
        """
        header = next(csv_reader)
        print(
            TerminalColors.info(
                f"Header: {TerminalColors.highlight_value('|'.join(header))}"
            )
        )
        return header
