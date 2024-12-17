import json
import subprocess
from datetime import datetime

def get_instance_info(instance_id):
    """Call the get_instance_info.py script to fetch instance details."""
    try:
        # Call the get_instance_info.py script with the instance ID as an argument
        result = subprocess.run(
            ['python3', 'get_instance_info.py', instance_id],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            # Parse the output from the script (JSON formatted)
            instance_info = json.loads(result.stdout)
            return instance_info
        else:
            print(f"Error executing get_instance_info.py: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error retrieving instance information: {e}")
        return None

def append_to_permission_log(data, log_file='permission_log.json'):
    """Append data to the permission_log.json file."""
    try:
        # Load existing log or initialize an empty list if the file doesn't exist
        try:
            with open(log_file, 'r') as f:
                log_data = json.load(f)
        except FileNotFoundError:
            log_data = []

        # Append the new data (with the current timestamp)
        data['Timestamp'] = datetime.utcnow().isoformat()
        log_data.append(data)

        # Write the updated data back to the file
        with open(log_file, 'w') as f:
            json.dump(log_data, f, indent=2)

        print(f"Instance information appended to {log_file}")
    
    except Exception as e:
        print(f"Error appending to {log_file}: {e}")

def lambda_handler(event, context):
    try:
        # Get the event name
        event_name = event.get("detail", {}).get("eventName", "")

        # Initialize variables
        resource_id = None
        valid = False

        # Check if the event name is relevant
        if event_name in ["CreateTags", "DeleteTags", "RunInstances", "StartInstances", "StopInstances"]:
            if event_name in ["CreateTags", "DeleteTags"]:
                # Navigate to the resource ID in the resourcesSet
                resource_items = event.get("detail", {}).get("requestParameters", {}).get("resourcesSet", {}).get("items", [])

                # Extract the single resource ID (if any)
                if resource_items:
                    resource_id = resource_items[0].get("resourceId")

                # Set validity based on the event name
                valid = event_name == "CreateTags" and resource_id is not None

            elif event_name == "RunInstances":
                # Navigate to the instance ID in the instancesSet
                instance_items = event.get("detail", {}).get("responseElements", {}).get("instancesSet", {}).get("items", [])

                # Extract the single instance ID (if any)
                if instance_items:
                    resource_id = instance_items[0].get("instanceId")

                # RunInstances events are always valid if resource ID exists
                valid = resource_id is not None

            elif event_name in ["StartInstances", "StopInstances"]:
                # Navigate to the instance ID in the instancesSet
                instance_items = event.get("detail", {}).get("responseElements", {}).get("instancesSet", {}).get("items", [])

                # Extract the single instance ID (if any)
                if instance_items:
                    resource_id = instance_items[0].get("instanceId")

                # StartInstances is valid, StopInstances is not, only if resource ID exists
                valid = resource_id is not None and event_name == "StartInstances"

        # Print extracted resource ID and validity
        print("Event Name:", event_name)
        print("Extracted Resource ID:", resource_id)
        print("Validity:", valid)

        # If valid, fetch instance information and append to the permission log
        if resource_id:
            instance_info = get_instance_info(resource_id)
            if instance_info:
                # Print the instance IP and Tags
                print(f"Private IP Address: {instance_info.get('PrivateIpAddress')}")
                print(f"Public IP Address: {instance_info.get('PublicIpAddress')}")
                print(f"Tags: {instance_info.get('Tags')}")

                # Append to the log
                append_to_permission_log(instance_info)

                # Include IP addresses in the return message
                return_ip_info = {
                    "PrivateIpAddress": instance_info.get("PrivateIpAddress"),
                    "PublicIpAddress": instance_info.get("PublicIpAddress")
                }

                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": "Resource ID extracted successfully and logged!",
                        "eventName": event_name,
                        "resourceId": resource_id,
                        "valid": valid,
                        "ipInfo": return_ip_info
                    })
                }

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "No valid instance found to log.",
                "eventName": event_name,
                "resourceId": resource_id,
                "valid": valid
            })
        }

    except Exception as e:
        print("Error occurred:", e)
        return {
            "statusCode": 500,
            "body": json.dumps({
                "message": "An error occurred.",
                "error": str(e)
            })
        }
