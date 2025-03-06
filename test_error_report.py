from src.utils.error_collector import ErrorCollector
from http.server import HTTPServer, SimpleHTTPRequestHandler
import webbrowser
import os

def generate_sample_errors():
    collector = ErrorCollector()
    
    # Add some sample header errors
    collector.add_error("header", "structure", "Column Order", "Required column 'Date' is missing")
    collector.add_error("header", "format", "Column Names", "Column name 'customer_ID' should be 'Customer_ID'")
    
    # Add some content errors
    collector.add_error("content", "data_type", "Amount", "Invalid numeric value 'abc'", row=5)
    collector.add_error("content", "data_type", "Amount", "Invalid numeric value 'xyz'", row=8)
    collector.add_error("content", "required", "Customer_ID", "Value cannot be empty", row=12)
    collector.add_error("content", "range", "Amount", "Value must be positive", row=15)
    
    # Add some footer errors
    collector.add_error("footer", "checksum", "Total", "Footer total doesn't match content sum")
    collector.add_error("footer", "structure", "Summary", "Missing required summary section")
    
    # Add some PM validation errors
    collector.add_error("PM validation", "business_rules", "Transaction_Type", "Invalid transaction type 'XYZ'", row=20)
    collector.add_error("PM validation", "consistency", "Amount", "Amount exceeds daily limit", row=25)
    
    return collector

def main():
    # Generate error report
    collector = generate_sample_errors()
    report_path = collector.generate_html_report()
    
    # Get the absolute path to the report
    abs_report_path = os.path.abspath(report_path)
    print(f"Report generated at: {abs_report_path}")
    
    # Change to the directory containing the report
    os.chdir(os.path.dirname(abs_report_path))
    
    # Start HTTP server
    server_address = ('', 8000)
    httpd = HTTPServer(server_address, SimpleHTTPRequestHandler)
    print("Server started at http://localhost:8000")
    print(f"View report at: http://localhost:8000/{os.path.basename(report_path)}")
    httpd.serve_forever()

if __name__ == "__main__":
    main()
