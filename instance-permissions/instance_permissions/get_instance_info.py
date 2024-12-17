import boto3
import json
import sys

def get_instance_info(instance_id):
    """Get details about an EC2 instance, including its IP address and tags."""
    # Create a session using default credentials
    ec2 = boto3.client('ec2')

    try:
        # Call EC2 to retrieve instance details
        response = ec2.describe_instances(InstanceIds=[instance_id])

        # Extract instance information
        instance = response['Reservations'][0]['Instances'][0]
        instance_info = {
            'InstanceId': instance['InstanceId'],
            'InstanceType': instance.get('InstanceType', 'N/A'),
            'PrivateIpAddress': instance.get('PrivateIpAddress', 'N/A'),
            'PublicIpAddress': instance.get('PublicIpAddress', 'N/A'),
            'Tags': instance.get('Tags', [])
        }

        return instance_info

    except Exception as e:
        print(f"Error retrieving instance information: {e}")
        return None

def save_instance_info(instance_info, file_name):
    """Save the instance information to a JSON file."""
    try:
        with open(file_name, 'w') as f:
            json.dump(instance_info, f, indent=2)
        print(f"Instance information saved to {file_name}")
    except Exception as e:
        print(f"Error saving instance information to {file_name}: {e}")

def main():
    """Main function to handle input and execution flow."""
    if len(sys.argv) != 2:
        print("Usage: python get_instance_info.py <InstanceId>")
        sys.exit(1)

    instance_id = sys.argv[1]
    
    # Fetch instance information
    instance_info = get_instance_info(instance_id)
    
    if instance_info:
        # Save to a file (or do something else with it)
        save_instance_info(instance_info, f"{instance_id}_info.json")

if __name__ == "__main__":
    main()
