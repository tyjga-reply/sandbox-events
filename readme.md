#Quick Code to send events on the aws eventbridge

#Using AWS-Vault:

#CLI:
aws-vault exec PROFILE -- python3 sendevent.py

##############################################################

#Personal:
aws-vault exec sandbox -- python3 sendevent.py

##############################################################
#Run Tests like this:
sam build
sam local invoke InstanceDecisionFunction -e events/runInstance.json
    ##When Error "app is missing":
    rm -rf .aws-sam/  
