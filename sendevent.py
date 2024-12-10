import boto3
import json
import datetime

client = boto3.client('events', region_name='us-east-1')

event_payload = {
    'Entries': [
        {
            'Time': datetime.datetime.now(datetime.timezone.utc),
            'EventBusName': 'default', # default is not required
            'Source': 'custom.ec2.simulator',
            'DetailType': 'EC2 Instance State-change Notification',
            'Resources': [], # not required
            'Detail': json.dumps({
                'instance-id': 'i-00000000000000', # not required
                'state': 'running'
            })
        }
    ]
}

try:
    response = client.put_events(**event_payload)
    print("Event sent successfully!")
    print(response)
except Exception as e:
    print(f"Error sending event: {e}")
