"""
Error collection and reporting utilities.

This module provides functionality for collecting, categorizing, and reporting validation
errors in a structured format that improves readability and organization.
"""
from collections import defaultdict
import os
from datetime import datetime
import json
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
            lambda: defaultdict(
                lambda: defaultdict(list)
            )
        )
        self.error_count: int = 0
        self.has_errors: bool = False
    
    def add_error(self, section: str, error_type: str, field: str, message: str, row: Optional[int] = None) -> None:
        """
        Add an error to the collection.
        
        Args:
            section: The section where the error occurred (header, content, footer, PM validation)
            error_type: Type of error (structure, format, etc.)
            field: Field or column name where the error was found
            message: Detailed error message
            row: Optional row number for content errors
        """
        error_info: ErrorInfo = {
            'message': message,
            'row': row
        }
        
        self.errors[section][error_type][field].append(error_info)
        self.error_count += 1
        self.has_errors = True
    
    def get_error_count(self) -> int:
        """Return the total number of errors collected."""
        return self.error_count
    
    def get_summary(self) -> Dict[str, Union[int, Dict[str, Dict[str, Union[int, Dict[str, int]]]]]]:
        """Generate a summary of errors by category."""
        summary: Dict[str, Union[int, Dict[str, Dict[str, Union[int, Dict[str, int]]]]]] = {
            'total_errors': self.error_count,
            'sections': {}
        }
        
        for section, type_errors in self.errors.items():
            section_count = sum(len(errors) 
                             for error_type in type_errors.values() 
                             for _, errors in error_type.items())
            
            if isinstance(summary['sections'], dict):
                summary['sections'][section] = {
                    'count': section_count,
                    'types': {}
                }
            
                for error_type, field_errors in type_errors.items():
                    type_count = sum(len(errors) for _, errors in field_errors.items())
                    types_dict = summary['sections'][section].get('types')
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
            section_count = sum(len(errors) 
                             for error_type in type_errors.values() 
                             for _, errors in error_type.items())
            
            print(f"\n== {section.upper()} ({section_count} errors) ==")
            
            for error_type, field_errors in type_errors.items():
                type_count = sum(len(errors) for _, errors in field_errors.items())
                print(f"\n-- {error_type} ({type_count} errors) --")
                
                for field_name, errors in field_errors.items():
                    print(f"\n{field_name} ({len(errors)} errors):")
                    
                    # Group errors by message to avoid repetition
                    grouped_errors: DefaultDict[str, List[int]] = defaultdict(list)
                    for error in errors:
                        key = str(error['message'])
                        if error['row'] is not None:
                            grouped_errors[key].append(int(error['row']))
                        else:
                            grouped_errors[key] = []
                    
                    for message, rows in grouped_errors.items():
                        if rows:
                            # Only show first few rows if there are many
                            if len(rows) > 5:
                                row_display = f"Rows {', '.join(map(str, rows[:5]))}... and {len(rows)-5} more"
                            else:
                                row_display = f"Rows {', '.join(map(str, rows))}"
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
            # Create a timestamped filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filepath = os.path.join(os.getcwd(), f"validation_report_{timestamp}.html")
        
        html: List[str] = []
        
        # HTML header and style
        html.append("""<!DOCTYPE html>
<html>
<head>
    <title>CSV Validation Error Report</title>
    <style>
        body {
            font-family: Arial, sans-serif;
            margin: 20px;
            line-height: 1.6;
        }
        h1 {
            color: #2c3e50;
            border-bottom: 2px solid #3498db;
            padding-bottom: 10px;
        }
        h2 {
            color: #2c3e50;
            margin-top: 30px;
            background-color: #ecf0f1;
            padding: 8px;
            border-radius: 5px;
        }
        h3 {
            color: #3498db;
            margin-top: 20px;
        }
        h4 {
            margin-top: 15px;
            margin-bottom: 5px;
            color: #7f8c8d;
        }
        .error-card {
            background-color: #f9f9f9;
            border-left: 4px solid #e74c3c;
            padding: 10px;
            margin: 10px 0;
            border-radius: 0 5px 5px 0;
        }
        .error-message {
            font-weight: bold;
            color: #e74c3c;
        }
        .error-locations {
            color: #7f8c8d;
            font-style: italic;
            margin-top: 5px;
        }
        .summary {
            background-color: #f9f9f9;
            padding: 15px;
            border-radius: 5px;
            margin-bottom: 20px;
        }
        .summary-item {
            margin: 5px 0;
        }
        .no-errors {
            color: #27ae60;
            font-weight: bold;
        }
        .collapsible {
            background-color: #f1f1f1;
            color: #444;
            cursor: pointer;
            padding: 10px;
            width: 100%;
            border: none;
            text-align: left;
            outline: none;
            font-size: 15px;
            border-radius: 5px;
            margin-top: 5px;
        }
        .active, .collapsible:hover {
            background-color: #e0e0e0;
        }
        .content {
            padding: 0 18px;
            display: none;
            overflow: hidden;
            background-color: #ffffff;
            border-radius: 0 0 5px 5px;
        }
    </style>
</head>
<body>
    <h1>CSV Validation Error Report</h1>
    <div class="summary">
        <h3>Summary</h3>""")
        
        # Summary section
        if not self.has_errors:
            html.append('<p class="no-errors">No validation errors found!</p>')
        else:
            html.append(f'<p class="summary-item"><strong>Total Errors:</strong> {self.error_count}</p>')
            
            summary = self.get_summary()
            
            # Add explicit typing and careful handling of dictionary access
            if isinstance(summary['sections'], dict):
                sections_dict = summary['sections']
                
                for section_name, section_data in sections_dict.items():
                    if 'count' in section_data:
                        # Safe access to section count
                        section_count = section_data.get('count', 0)
                        html.append(f'<p class="summary-item"><strong>{section_name.upper()}:</strong> {section_count} errors</p>')
                        html.append('<ul>')
                        
                        # Safe access to types dictionary
                        if 'types' in section_data:
                            types_dict = section_data['types']
                            if isinstance(types_dict, dict):
                                for error_type, count in types_dict.items():
                                    html.append(f'<li>{error_type}: {count} errors</li>')
                        html.append('</ul>')
        
        html.append('</div>')  # Close summary div
        
        # Detailed error sections
        if self.has_errors:
            for section, type_errors in self.errors.items():
                section_count = sum(len(errors) 
                                for error_type in type_errors.values() 
                                for _, errors in error_type.items())
                
                html.append(f'<h2>{section.upper()} ({section_count} errors)</h2>')
                
                for error_type, field_errors in type_errors.items():
                    type_count = sum(len(errors) for _, errors in field_errors.items())
                    html.append(f'<button class="collapsible">{error_type} ({type_count} errors)</button>')
                    html.append('<div class="content">')
                    
                    for field_name, errors in field_errors.items():
                        html.append(f'<h4>{field_name} ({len(errors)} errors):</h4>')
                        
                        # Group errors by message to avoid repetition
                        grouped_errors: DefaultDict[str, List[int]] = defaultdict(list)
                        for error in errors:
                            key = str(error['message'])
                            if error['row'] is not None:
                                grouped_errors[key].append(int(error['row']))
                            else:
                                grouped_errors[key] = []
                        
                        for message, rows in grouped_errors.items():
                            html.append('<div class="error-card">')
                            html.append(f'<div class="error-message">{message}</div>')
                            
                            if rows:
                                # If there are many rows, only show first few
                                if len(rows) > 10:
                                    rows_str = ", ".join(map(str, sorted(rows)[:10])) + f"... and {len(rows)-10} more"
                                else:
                                    rows_str = ", ".join(map(str, sorted(rows)))
                                
                                html.append(f'<div class="error-locations">Rows: {rows_str}</div>')
                            
                            html.append('</div>')  # Close error-card div
                    
                    html.append('</div>')  # Close content div
        
        # JavaScript for collapsible sections
        html.append("""
    <script>
        var coll = document.getElementsByClassName("collapsible");
        for (var i = 0; i < coll.length; i++) {
            coll[i].addEventListener("click", function() {
                this.classList.toggle("active");
                var content = this.nextElementSibling;
                if (content.style.display === "block") {
                    content.style.display = "none";
                } else {
                    content.style.display = "block";
                }
            });
        }
    </script>
</body>
</html>""")
        
        # Write the HTML file
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write('\n'.join(html))
        
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
        export_data: Dict[str, Union[str, int, Dict[str, Union[int, Dict[str, Dict[str, Union[int, Dict[str, int]]]]]], Dict[str, Dict[str, Dict[str, List[ErrorInfo]]]]]] = {
            'timestamp': datetime.now().isoformat(),
            'total_errors': self.error_count,
            'summary': self.get_summary(),
            'errors': errors_dict
        }
        
        # Write to file
        with open(filepath, 'w', encoding='utf-8') as f:
            json.dump(export_data, f, indent=2, default=str)
        
        return filepath
