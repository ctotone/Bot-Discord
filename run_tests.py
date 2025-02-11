import pytest
import sys
import os
from datetime import datetime

def run_tests():
    """Run all tests and generate a report"""
    # Create test results directory if it doesn't exist
    if not os.path.exists('test_results'):
        os.makedirs('test_results')

    # Generate timestamp for report file
    timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
    report_file = f'test_results/test_report_{timestamp}.txt'

    # Run tests with pytest
    arguments = [
        'tests',
        '-v',
        '--tb=short',
        f'--junitxml=test_results/junit_{timestamp}.xml',
    ]

    # Capture the test results
    exit_code = pytest.main(arguments)

    # Generate summary report
    with open(report_file, 'w') as f:
        f.write(f"Bot Testing Report - {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n")
        f.write("=" * 50 + "\n\n")
        
        if exit_code == 0:
            f.write("All tests passed successfully!\n")
        else:
            f.write(f"Some tests failed (exit code: {exit_code})\n")
        
        f.write("\nTest Categories:\n")
        f.write("- Bot Commands\n")
        f.write("- Bot Connection\n")
        f.write("- Bot Events\n")

    print(f"Test report generated: {report_file}")
    return exit_code

if __name__ == '__main__':
    sys.exit(run_tests())
