"""
Includes methods for teardown of the validations
"""
from src.utils.terminal_colors import TerminalColors


class Teardown:
    """
    Class for organizing teardown methods
    """

    @staticmethod
    def generate_output(args, error_collector):
        """
        Method for file saving of the results and creating output
        """
        # Generate appropriate output based on format argument
        if args.format == "terminal" or args.format == "all":
            error_collector.print_terminal_report()

        if args.format == "html" or args.format == "all":
            html_path = error_collector.generate_html_report()
            print(f"\nHTML report generated: {html_path}")

        if args.format == "json" or args.format == "all":
            json_path = error_collector.export_json()
            print(f"\nJSON export generated: {json_path}")

        # Final message indicating completion of the validation process
        print(TerminalColors.success("Validation complete."))
        print(TerminalColors.section_end())
