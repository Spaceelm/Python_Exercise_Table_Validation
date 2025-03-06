"""
Error collection and reporting utilities.

This module provides functionality for collecting, categorizing, and reporting validation
errors in a structured format that improves readability and organization.
"""
import json
import os
from collections import defaultdict
from datetime import datetime
from typing import Dict, List, Optional, Union, DefaultDict

# Define type aliases to make the nested structure clearer
ErrorInfo = Dict[str, Optional[Union[str, int]]]
FieldErrors = DefaultDict[str, List[ErrorInfo]]
TypeErrors = DefaultDict[str, FieldErrors]
SectionErrors = DefaultDict[str, TypeErrors]


class ErrorCollector:
    """
    Class for collecting and organizing validation errors.

    This class provides methods for adding errors, categorizing them,
    and generating reports in different formats (terminal, HTML).
    """

    def __init__(self):
        """Initialize the error collector with empty collections."""
        # Main storage structure - nested defaultdicts
        self.errors: SectionErrors = defaultdict(
            lambda: defaultdict(lambda: defaultdict(list))
        )
        self.error_count: int = 0
        self.has_errors: bool = False
        self.validation_rules: Dict[str, Dict[str, str]] = {
            "header": {
                "structure": "Header must contain all required columns in correct order",
                "format": "Header fields must follow naming conventions",
            },
            "content": {
                "data_type": "Field values must match expected data types",
                "format": "Content must follow specified format rules",
                "required": "Required fields must not be empty",
                "range": "Numeric values must be within valid ranges",
            },
            "footer": {
                "structure": "Footer must contain required summary information",
                "checksum": "Footer checksums must match content",
            },
            "PM validation": {
                "business_rules": "Data must comply with PM-specific business rules",
                "consistency": "Data must be consistent across related fields",
            }
        }

    def add_error(
        self,
        section: str,
        error_type: str,
        field: str,
        message: str,
        row: Optional[int] = None,
    ) -> None:
        """
        Add an error to the collection.

        Args:
            section: The section where the error occurred (header, content, footer, PM validation)
            error_type: Type of error (structure, format, etc.)
            field: Field or column name where the error was found
            message: Detailed error message
            row: Optional row number for content errors
        """
        error_info: ErrorInfo = {"message": message, "row": row}

        self.errors[section][error_type][field].append(error_info)
        self.error_count += 1
        self.has_errors = True

    def get_error_count(self) -> int:
        """Return the total number of errors collected."""
        return self.error_count

    def get_summary(
        self,
    ) -> Dict[str, Union[int, Dict[str, Dict[str, Union[int, Dict[str, int]]]]]]:
        """Generate a summary of errors by category."""
        summary: Dict[
            str, Union[int, Dict[str, Dict[str, Union[int, Dict[str, int]]]]]
        ] = {"total_errors": self.error_count, "sections": {}}

        for section, type_errors in self.errors.items():
            section_count = sum(
                len(errors)
                for error_type in type_errors.values()
                for _, errors in error_type.items()
            )

            if isinstance(summary["sections"], dict):
                summary["sections"][section] = {"count": section_count, "types": {}}

                for error_type, field_errors in type_errors.items():
                    type_count = sum(len(errors) for _, errors in field_errors.items())
                    types_dict = summary["sections"][section].get("types")
                    if isinstance(types_dict, dict):
                        types_dict[error_type] = type_count

        return summary

    def print_terminal_report(self) -> None:
        """Print a formatted error report to the terminal."""
        if not self.has_errors:
            print("No validation errors found!")
            return

        print(f"\n===== VALIDATION ERROR REPORT ({self.error_count} errors) =====\n")

        for section, type_errors in self.errors.items():
            section_count = sum(
                len(errors)
                for error_type in type_errors.values()
                for _, errors in error_type.items()
            )

            print(f"\n== {section.upper()} ({section_count} errors) ==")

            for error_type, field_errors in type_errors.items():
                type_count = sum(len(errors) for _, errors in field_errors.items())
                print(f"\n-- {error_type} ({type_count} errors) --")

                for field_name, errors in field_errors.items():
                    print(f"\n{field_name} ({len(errors)} errors):")

                    # Group errors by message to avoid repetition
                    grouped_errors: DefaultDict[str, List[int]] = defaultdict(list)
                    for error in errors:
                        key = str(error["message"])
                        if error["row"] is not None:
                            grouped_errors[key].append(int(error["row"]))
                        else:
                            grouped_errors[key] = []

                    for message, rows in grouped_errors.items():
                        if rows:
                            # Only show first few rows if there are many
                            if len(rows) > 5:
                                row_display = (
                                    ", ".join(map(str, rows[:5]))
                                    + f"... and {len(rows) - 5} more"
                                )
                            else:
                                row_display = ", ".join(map(str, rows))

                            print(f"  - {message} ({row_display})")
                        else:
                            print(f"  - {message}")

    def generate_html_report(self, filepath: Optional[str] = None) -> str:
        """
        Generate an HTML report of the errors.

        Args:
            filepath: Optional path to save the report to. If not provided,
                     will save to 'validation_report_YYYYMMDD_HHMMSS.html'
                     in the current directory.

        Returns:
            str: Path to the generated HTML file
        """
        if filepath is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(os.getcwd(), f"validation_report_{timestamp}.html")

        html: List[str] = [
            """<!DOCTYPE html>
<html>
<head>
    <title>CSV Validation Error Report</title>
    <style>
        :root {
            --primary-color: #2c3e50;
            --secondary-color: #3498db;
            --success-color: #27ae60;
            --error-color: #e74c3c;
            --warning-color: #f39c12;
            --bg-light: #f9f9f9;
            --bg-dark: #ecf0f1;
        }
        body {
            font-family: 'Segoe UI', Arial, sans-serif;
            margin: 0;
            padding: 20px;
            line-height: 1.6;
            color: var(--primary-color);
            background-color: #f5f6fa;
        }
        .container {
            max-width: 1200px;
            margin: 0 auto;
            background-color: white;
            padding: 20px;
            border-radius: 10px;
            box-shadow: 0 2px 10px rgba(0,0,0,0.1);
        }
        h1 {
            color: var(--primary-color);
            border-bottom: 3px solid var(--secondary-color);
            padding-bottom: 10px;
            margin-bottom: 30px;
        }
        .timestamp {
            color: #666;
            font-size: 0.9em;
            margin-bottom: 20px;
        }
        .section {
            margin: 30px 0;
            padding: 20px;
            background-color: white;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .section-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 15px;
        }
        .section-title {
            color: var(--primary-color);
            margin: 0;
            font-size: 1.5em;
        }
        .error-count {
            background-color: var(--error-color);
            color: white;
            padding: 5px 10px;
            border-radius: 15px;
            font-size: 0.9em;
        }
        .validation-rules {
            background-color: var(--bg-light);
            padding: 15px;
            border-radius: 8px;
            margin: 20px 0;
        }
        .rule-category {
            margin: 10px 0;
            padding: 10px;
            background-color: white;
            border-radius: 5px;
            border-left: 4px solid var(--secondary-color);
        }
        .error-card {
            background-color: white;
            border-left: 4px solid var(--error-color);
            padding: 15px;
            margin: 10px 0;
            border-radius: 5px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .error-message {
            font-weight: 500;
            color: var(--error-color);
            margin-bottom: 8px;
        }
        .error-details {
            font-size: 0.9em;
            color: #666;
        }
        .error-locations {
            background-color: var(--bg-light);
            padding: 5px 10px;
            border-radius: 4px;
            margin-top: 8px;
            font-family: monospace;
        }
        .collapsible {
            background-color: var(--bg-light);
            color: var(--primary-color);
            cursor: pointer;
            padding: 15px;
            width: 100%;
            border: none;
            text-align: left;
            outline: none;
            font-size: 1em;
            border-radius: 5px;
            margin-top: 10px;
            transition: background-color 0.3s;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }
        .collapsible:after {
            content: '\\002B';
            font-weight: bold;
            float: right;
            margin-left: 5px;
        }
        .active:after {
            content: '\\2212';
        }
        .active, .collapsible:hover {
            background-color: var(--bg-dark);
        }
        .content {
            padding: 0 18px;
            max-height: 0;
            overflow: hidden;
            transition: max-height 0.2s ease-out;
            background-color: white;
            border-radius: 0 0 5px 5px;
        }
        .summary {
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
            gap: 20px;
            margin-bottom: 30px;
        }
        .summary-card {
            background-color: white;
            padding: 20px;
            border-radius: 8px;
            box-shadow: 0 2px 5px rgba(0,0,0,0.05);
        }
        .no-errors {
            color: var(--success-color);
            font-weight: bold;
            text-align: center;
            padding: 20px;
            background-color: #f0fff4;
            border-radius: 8px;
            margin: 20px 0;
        }
        @media (max-width: 768px) {
            .container {
                padding: 10px;
            }
            .summary {
                grid-template-columns: 1fr;
            }
        }
    </style>
</head>
<body>
    <div class="container">
        <h1>CSV Validation Error Report</h1>
        <div class="timestamp">Generated on: """ + datetime.now().strftime("%Y-%m-%d %H:%M:%S") + """</div>"""
        ]

        # Summary section
        if not self.has_errors:
            html.append('<div class="no-errors">✓ No validation errors found!</div>')
        else:
            html.append('<div class="summary">')
            summary = self.get_summary()

            # Total errors card
            html.append(f'''
                <div class="summary-card">
                    <h3>Total Errors</h3>
                    <div class="error-count">{self.error_count}</div>
                </div>
            ''')

            # Section-wise summary
            if isinstance(summary["sections"], dict):
                sections_dict = summary["sections"]
                for section_name, section_data in sections_dict.items():
                    if isinstance(section_data, dict) and "count" in section_data:
                        section_count = section_data["count"]
                        html.append(f'''
                            <div class="summary-card">
                                <h3>{section_name.upper()}</h3>
                                <div class="error-count">{section_count}</div>
                                <div class="error-details">
                        ''')
                        
                        if "types" in section_data:
                            types_dict = section_data["types"]
                            if isinstance(types_dict, dict):
                                for error_type, count in types_dict.items():
                                    html.append(f'<div>{error_type}: {count}</div>')
                        
                        html.append('</div></div>')

            html.append('</div>')  # Close summary div

            # Validation Rules Section
            html.append('''
                <div class="section">
                    <div class="section-header">
                        <h2 class="section-title">Validation Rules</h2>
                    </div>
                    <div class="validation-rules">
            ''')
            
            for section, rules in self.validation_rules.items():
                html.append(f'''
                    <div class="rule-category">
                        <h3>{section.upper()}</h3>
                        <ul>
                ''')
                for rule_type, description in rules.items():
                    html.append(f'<li><strong>{rule_type}:</strong> {description}</li>')
                html.append('</ul></div>')
            
            html.append('</div></div>')  # Close validation rules section

            # Detailed error sections
            for section, type_errors in self.errors.items():
                section_count = sum(
                    len(errors)
                    for error_type in type_errors.values()
                    for _, errors in error_type.items()
                )

                html.append(f'''
                    <div class="section">
                        <div class="section-header">
                            <h2 class="section-title">{section.upper()}</h2>
                            <span class="error-count">{section_count} errors</span>
                        </div>
                ''')

                for error_type, field_errors in type_errors.items():
                    type_count = sum(len(errors) for _, errors in field_errors.items())
                    html.append(
                        f'<button class="collapsible">{error_type} <span class="error-count">{type_count}</span></button>'
                    )
                    html.append('<div class="content">')

                    for field_name, errors in field_errors.items():
                        html.append(f'''
                            <div class="field-errors">
                                <h4>{field_name} ({len(errors)} errors):</h4>
                        ''')

                        # Group errors by message
                        grouped_errors: DefaultDict[str, List[int]] = defaultdict(list)
                        for error in errors:
                            key = str(error["message"])
                            if error["row"] is not None:
                                grouped_errors[key].append(int(error["row"]))
                            else:
                                grouped_errors[key] = []

                        for message, rows in grouped_errors.items():
                            html.append('<div class="error-card">')
                            html.append(f'<div class="error-message">{message}</div>')

                            if rows:
                                rows_sorted = sorted(rows)
                                if len(rows) > 10:
                                    rows_display = (
                                        ", ".join(map(str, rows_sorted[:10]))
                                        + f" <em>and {len(rows) - 10} more...</em>"
                                    )
                                else:
                                    rows_display = ", ".join(map(str, rows_sorted))

                                html.append(
                                    f'<div class="error-locations">Rows: {rows_display}</div>'
                                )

                            html.append("</div>")  # Close error-card

                        html.append("</div>")  # Close field-errors
                    html.append("</div>")  # Close content
                html.append("</div>")  # Close section

        # JavaScript for collapsible sections
        html.append(
            """
        <script>
            var coll = document.getElementsByClassName("collapsible");
            for (var i = 0; i < coll.length; i++) {
                coll[i].addEventListener("click", function() {
                    this.classList.toggle("active");
                    var content = this.nextElementSibling;
                    if (content.style.maxHeight) {
                        content.style.maxHeight = null;
                    } else {
                        content.style.maxHeight = content.scrollHeight + "px";
                    }
                });
            }
        </script>
    </div>
</body>
</html>"""
        )

        # Write the HTML file
        with open(filepath, "w", encoding="utf-8") as f:
            f.write("\n".join(html))

        return filepath

    def export_json(self, filepath: Optional[str] = None) -> str:
        """
        Export errors to a JSON file.

        Args:
            filepath: Optional path to save the JSON to. If not provided,
                     will save to 'validation_errors_YYYYMMDD_HHMMSS.json'
                     in the current directory.

        Returns:
            str: Path to the generated JSON file
        """
        if filepath is None:
            # Create a timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(os.getcwd(), f"validation_errors_{timestamp}.json")

        # Convert defaultdict to regular dict for JSON serialization
        errors_dict: Dict[str, Dict[str, Dict[str, List[ErrorInfo]]]] = {}
        for section, type_errors in self.errors.items():
            errors_dict[section] = {}
            for error_type, field_errors in type_errors.items():
                errors_dict[section][error_type] = {}
                for field, errors in field_errors.items():
                    errors_dict[section][error_type][field] = errors

        # Create a JSON object with metadata
        export_data: Dict[
            str,
            Union[
                str,
                int,
                Dict[str, Union[int, Dict[str, Dict[str, Union[int, Dict[str, int]]]]]],
                Dict[str, Dict[str, Dict[str, List[ErrorInfo]]]],
            ],
        ] = {
            "timestamp": datetime.now().isoformat(),
            "total_errors": self.error_count,
            "summary": self.get_summary(),
            "errors": errors_dict,
        }

        # Write to file
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(export_data, f, indent=2, default=str)

        return filepath
