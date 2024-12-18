import json
import subprocess

TAG_KEY = "permission"
TAG_VALUE = "yes"

def get_instance_info(instance_id):
    """Call the get_instance_info.py script to fetch instance details."""
    try:
        result = subprocess.run(
            ['python3', 'get_instance_info.py', instance_id],
            capture_output=True,
            text=True
        )

        if result.returncode == 0:
            instance_info = json.loads(result.stdout)
            return instance_info
        else:
            print(f"Error executing get_instance_info.py: {result.stderr}")
            return None
    except Exception as e:
        print(f"Error retrieving instance information: {e}")
        return None

def lambda_handler(event, context):
    try:
        event_name = event.get("detail", {}).get("eventName", "")

        # Initialize variables
        resource_id = None
        valid = False

        # Check if relevant event name
        if event_name in ["CreateTags", "DeleteTags", "RunInstances", "StartInstances", "StopInstances"]:
            if event_name in ["CreateTags", "DeleteTags"]:
                resource_items = event.get("detail", {}).get("requestParameters", {}).get("resourcesSet", {}).get("items", [])

                if resource_items:
                    resource_id = resource_items[0].get("resourceId")

            elif event_name == "RunInstances":
                instance_items = event.get("detail", {}).get("responseElements", {}).get("instancesSet", {}).get("items", [])

                if instance_items:
                    resource_id = instance_items[0].get("instanceId")

            elif event_name in ["StartInstances", "StopInstances"]:
                instance_items = event.get("detail", {}).get("responseElements", {}).get("instancesSet", {}).get("items", [])

                if instance_items:
                    resource_id = instance_items[0].get("instanceId")

        print("Event Name:", event_name)
        print("Extracted Resource ID:", resource_id)

        if resource_id:
            instance_info = get_instance_info(resource_id)
            if instance_info:
                print(f"Private IP Address: {instance_info.get('PrivateIpAddress')}")
                print(f"Tags: {instance_info.get('Tags')}")

                # Check if the tag key and value match
                tags = instance_info.get("Tags", [])
                tag_found = any(tag.get("Key") == TAG_KEY and tag.get("Value") == TAG_VALUE for tag in tags)

                # Set validity
                if not tag_found:
                    valid = False
                elif tag_found:
                    valid = True

                # Include IP addresses in the return message
                return_ip_info = {
                    "PrivateIpAddress": instance_info.get("PrivateIpAddress")
                }

                return {
                    "statusCode": 200,
                    "body": json.dumps({
                        "message": "Resource ID extracted successfully!",
                        "eventName": event_name,
                        "resourceId": resource_id,
                        "valid": valid,
                        "ipInfo": return_ip_info
                    })
                }

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "No valid instance found.",
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
