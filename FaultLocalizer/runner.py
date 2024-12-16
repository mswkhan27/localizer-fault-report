import argparse
from src.localizer import Localizer
from src.localizer import run_localizer

def parse_arguments():
    parser = argparse.ArgumentParser(description="Run Localizer with specific configurations.")
    parser.add_argument("--project_path", required=True, help="Path to the project.")
    parser.add_argument("--file_n", required=True, help="File name of the project.")
    parser.add_argument("--test_file", required=True, help="Path to the test file.")
    parser.add_argument("--outputFile", required=True, help="Output file for the fault summary.")
    parser.add_argument("--debug", action="store_true", help="Enable debug mode.")
    parser.add_argument("--entry_point", required=True, help="Entry point for the project.")
    parser.add_argument("--metric", required=True, help="Metric to be used.")
    return parser.parse_args()

if __name__ == "__main__":
    # Parse command line arguments
    args = parse_arguments()

    # Create the configuration dictionary from the command line arguments
    localizer_config = {
        "project_path": args.project_path,
        "file_n": args.file_n,
        "test_file": args.test_file,
        "outputFile": args.outputFile,
        "debug": args.debug,
        "entry_point": args.entry_point,
        "metric": args.metric
    }

    # Initialize and run the Localizer
    loc = Localizer(**localizer_config)
    run_localizer(loc)


'''
    localizer_configs = [
        {"project_path": "examples/multiply/", "file_n": "multiply.py", "test_file": "examples/multiply/tests/tests.txt", "outputFile": 'fault_summary.json', "debug": True, "entry_point": "multiply", "metric": 'savg'},
        {"project_path": "examples/power/", "file_n": "power.py", "test_file": "examples/power/tests/tests.txt", "outputFile": 'fault_summary.json', "debug": True, "entry_point": "power"},
        {"project_path": "examples/circles_overlap/", "file_n": "circles_overlap.py", "test_file": "examples/circles_overlap/tests/tests.txt", "outputFile": 'fault_summary.json', "debug": True, "entry_point": "circle_overlap_status"},
        {"project_path": "examples/hex_conversion/", "file_n": "hex_conversion.py", "test_file": "examples/hex_conversion/tests/tests.txt", "outputFile": 'fault_summary.json', "debug": True, "entry_point": "hex_conversion", "metric": 'savg'},
        {"project_path": "examples/next_day/", "file_n": "next_day.py", "test_file": "examples/next_day/tests/tests.txt", "outputFile": 'fault_summary.json', "debug": True, "entry_point": "get_next_date"},
        {"project_path": "examples/next_palindrome/", "file_n": "next_palindrome.py", "test_file": "examples/next_palindrome/tests.txt", "outputFile": 'fault_summary.json', "debug": True, "entry_point": "next_palindrome"},
        {"project_path": "examples/progression/", "file_n": "progression.py", "test_file": "examples/progression/tests/tests.txt", "outputFile": 'fault_summary.json', "debug": True, "entry_point": "ap_gp_sequence"},
        {"project_path": "examples/trityp/", "file_n": "trityp.py", "test_file": "examples/trityp/tests/tests.txt", "outputFile": 'fault_summary.json', "debug": True, "entry_point": "trityp"},
        {"project_path": "examples/mergesort/", "file_n": "mergesort.py", "test_file": "examples/mergesort/tests/tests.txt", "outputFile": 'fault_summary.json', "debug": True, "entry_point": "mergesort"},
        {"project_path": "examples/equilateral_area/", "file_n": "equilateral_area.py", "test_file": "examples/equilateral_area/tests/tests.txt", "outputFile": 'fault_summary.json', "debug": True, "entry_point": "equilateral_area"}
]
'''

#How to Run?
#e.g: python39 runner.py --project_path "examples/hex_conversion/" --file_n "hex_conversion.py" --test_file "examples/hex_conversion/tests/tests.txt" --outputFile "fault_summary.json" --debug --entry_point "hex_conversion" --metric "savg"