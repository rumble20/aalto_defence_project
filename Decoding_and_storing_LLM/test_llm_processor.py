from llm_processor import MilitaryReportFormatter, ReportType
import os

def test_military_formatter():
    # Initialize the formatter
    formatter = MilitaryReportFormatter()
    
    # Test data
    test_packet = {
        "action": "Advance to Position",
        "target_units": ["Alpha Squad", "Bravo Team"],
        "coordinates": {"x": 35.6895, "y": 139.6917},
        "timeframe": "0800Z",
        "priority": "HIGH"
    }
    
    # Test EOINCREP report
    print("\nTesting EOINCREP report:")
    report_content, file_path = formatter.format_and_save_report(test_packet, ReportType.EOINCREP)
    print(report_content)
    print(f"Report saved to: {file_path}")
    
    # Test CASEVAC report
    print("\nTesting CASEVAC report:")
    report_content, file_path = formatter.format_and_save_report(test_packet, ReportType.CASEVAC)
    print(report_content)
    print(f"Report saved to: {file_path}")
    
    # Test invalid data
    print("\nTesting invalid data:")
    invalid_packet = {
        "action": "Advance",
        "coordinates": {"x": 123.0},  # Missing y coordinate
        "timeframe": "0600Z",
        "priority": "HIGH"
    }
    report_content, file_path = formatter.format_and_save_report(invalid_packet)
    print(report_content)

if __name__ == "__main__":
    test_military_formatter()
