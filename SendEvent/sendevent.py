import boto3
import json
import datetime

client = boto3.client('events', region_name='us-east-1')

# Load event entries from the JSON file
with open('event_entries.json', 'r') as file:
    event_data = json.load(file)

# Set the "Time" to the current time for each entry
for entry in event_data['Entries']:
    entry['Time'] = datetime.datetime.now(datetime.timezone.utc)

# Send the event
try:
    response = client.put_events(**event_data)
    print("Event sent successfully!")
    print(response)
except Exception as e:
    print(f"Error sending event: {e}")
