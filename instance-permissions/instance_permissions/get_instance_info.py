import boto3
import json
import sys

def get_instance_info(instance_id):
    """Get details about an EC2 instance, including its IP address and tags."""
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
            'Tags': instance.get('Tags', [])
        }

        # Output the instance info as JSON
        print(json.dumps(instance_info, indent=2))

    except Exception as e:
        print(f"Error retrieving instance information: {e}")
        sys.exit(1)

def main():
    """Main function to handle input and execution flow."""
    if len(sys.argv) != 2:
        print("Usage: python get_instance_info.py <InstanceId>")
        sys.exit(1)

    instance_id = sys.argv[1]
    
    # Fetch and print instance information
    get_instance_info(instance_id)

if __name__ == "__main__":
    main()
