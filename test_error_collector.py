from src.utils.error_collector import ErrorCollector

# Create an instance of ErrorCollector
collector = ErrorCollector()

# Add some test errors
collector.add_error("header", "structure", "column_name", "Missing required column", None)
collector.add_error("content", "format", "date_field", "Invalid date format", 5)
collector.add_error("content", "format", "date_field", "Invalid date format", 7)
collector.add_error("footer", "validation", "total_count", "Total count mismatch", None)

# Print the report to terminal
print("\nTesting terminal report:")
collector.print_terminal_report()

# Get a summary
print("\nTesting summary:")
summary = collector.get_summary()
print(f"Total errors: {summary['total_errors']}")

# Check if sections exists and is a dictionary before using len()
if isinstance(summary['sections'], dict):
    print(f"Sections: {len(summary['sections'])}")
else:
    print(f"Sections: {summary['sections']}")

# Test JSON export (comment out if you don't want to create a file)
# json_path = collector.export_json()
# print(f"\nJSON exported to: {json_path}")

# Test HTML report (comment out if you don't want to create a file)
# html_path = collector.generate_html_report()
# print(f"\nHTML report generated at: {html_path}")
