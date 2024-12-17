import json

def lambda_handler(event, context):
    try:
        # Get the event name
        event_name = event.get("detail", {}).get("eventName", "")

        # Initialize variables
        resource_ids = []
        valid = False

        # Check if the event name is relevant
        if event_name in ["CreateTags", "DeleteTags", "RunInstances", "StartInstances", "StopInstances"]:
            if event_name in ["CreateTags", "DeleteTags"]:
                # Navigate to the resource ID in the resourcesSet
                resource_items = event.get("detail", {}).get("requestParameters", {}).get("resourcesSet", {}).get("items", [])

                # Extract resource IDs
                resource_ids = [item.get("resourceId") for item in resource_items]

                # Set validity based on the event name
                valid = event_name == "CreateTags"

            elif event_name == "RunInstances":
                # Navigate to the instance ID in the instancesSet
                instance_items = event.get("detail", {}).get("responseElements", {}).get("instancesSet", {}).get("items", [])

                # Extract instance IDs
                resource_ids = [item.get("instanceId") for item in instance_items]

                # RunInstances events are always valid
                valid = True

            elif event_name in ["StartInstances", "StopInstances"]:
                # Navigate to the instance ID in the instancesSet
                instance_items = event.get("detail", {}).get("responseElements", {}).get("instancesSet", {}).get("items", [])

                # Extract instance IDs
                resource_ids = [item.get("instanceId") for item in instance_items]

                # StartInstances is valid, StopInstances is not
                valid = event_name == "StartInstances"

        # Print extracted resource IDs and validity
        print("Event Name:", event_name)
        print("Extracted Resource IDs:", resource_ids)
        print("Validity:", valid)

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Resource IDs extracted successfully!",
                "eventName": event_name,
                "resourceIds": resource_ids,
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
