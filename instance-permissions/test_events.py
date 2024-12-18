import os
import subprocess
import json

# Constants for paths and function name
EVENTS_FOLDER = "./events"
LAMBDA_FUNCTION_NAME = "InstanceDecisionFunction"

def run_test(event_file):
    """Run SAM local invoke for a given event file."""
    try:
        # Construct the SAM command
        command = [
            "sam", "local", "invoke", LAMBDA_FUNCTION_NAME, "-e", event_file
        ]
        
        # Pass AWS credentials from the environment
        env = os.environ.copy()
        if not env.get("AWS_ACCESS_KEY_ID") or not env.get("AWS_SECRET_ACCESS_KEY"):
            print("Error: AWS credentials are not set in the environment.")
            return None
        
        result = subprocess.run(command, capture_output=True, text=True, env=env)
        
        # Check if the command was successful
        if result.returncode != 0:
            print(f"Error invoking function for {event_file}: {result.stderr}")
            return None
        
        # Parse the response JSON
        response = json.loads(result.stdout)
        return response
    except Exception as e:
        print(f"Error running test for {event_file}: {e}")
        return None

def validate_response(event_file, response):
    """Validate the response against expected output."""
    # Load the expected result (assuming a file named <event_file>_expected.json exists in the same folder)
    expected_file = event_file.replace(".json", "_expected.json")
    if not os.path.exists(expected_file):
        print(f"No expected result file found for {event_file}. Skipping validation.")
        return False
    
    with open(expected_file, "r") as f:
        expected_response = json.load(f)
    
    # Compare the response to the expected output
    if response == expected_response:
        print(f"Test passed for {event_file}")
        return True
    else:
        print(f"Test failed for {event_file}")
        print("Expected:", json.dumps(expected_response, indent=2))
        print("Got:", json.dumps(response, indent=2))
        return False

def run_all_tests():
    """Run all tests in the events folder."""
    if not os.path.exists(EVENTS_FOLDER):
        print(f"Error: Events folder not found at {EVENTS_FOLDER}")
        return

    # Traverse both WithTag and WithoutTag subfolders to find event files
    event_files = []
    for subfolder in ["WithTag", "WithoutTag"]:
        subfolder_path = os.path.join(EVENTS_FOLDER, subfolder)
        if os.path.exists(subfolder_path):
            event_files += [os.path.join(subfolder_path, f) for f in os.listdir(subfolder_path) if f.endswith(".json") and not f.endswith("_expected.json")]

    if not event_files:
        print("No event files found in WithTag or WithoutTag subfolders.")
        return

    passed_tests = 0
    total_tests = 0

    # Run tests for each event file
    for event_file in event_files:
        print(f"Running test for {event_file}...")
        response = run_test(event_file)
        if response is None:
            print(f"Skipping validation for {event_file} due to invocation error.")
            continue
        
        if validate_response(event_file, response):
            passed_tests += 1
        
        total_tests += 1
    
    print(f"\nTest Summary: {passed_tests}/{total_tests} tests passed.")

if __name__ == "__main__":
    run_all_tests()
