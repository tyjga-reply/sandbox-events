# Description
Code to set permissions for EC2 instances based on their tags.
Code will request information from the **AWS server** to extract the **current IP-Address* of the EC2-Instance and searches for a specific **Tag Value**.

# Testing
**AWS Env-variables** must be set.
Tests are in the events folder and are triggered by the **test_events.py** file.

Right now the EC2-Instances are not mocked, meaning they refer to real instances that have to be online for the tests to succeed.

# Deployment
sam build --guided