import json

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

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Resource ID extracted successfully!",
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
