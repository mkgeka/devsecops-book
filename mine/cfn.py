import boto3
import cfnresponse
import json


def lambda_handler(event, context):
    try:
        ssm = boto3.client('ssm')

        # Preset credentials to store in SSM Parameter Store
        username = event['ResourceProperties']['Username']
        password = event['ResourceProperties']['Password']

        # Storing username in SSM Parameter Store
        ssm.put_parameter(
            Name='/rds/username',
            Value=username,
            Type='SecureString',
            Overwrite=True
        )

        # Storing password in SSM Parameter Store
        ssm.put_parameter(
            Name='/rds/secure-password',
            Value=password,
            Type='SecureString',
            Overwrite=True
        )

        # Prepare the response data
        response_data = {"Success": "Username and password parameters have been set successfully."}
        cfnresponse.send(event, context, cfnresponse.SUCCESS, response_data)
    except Exception as e:
        # Prepare the error message
        error_message = str(e)

        # Send failure response to CloudFormation
        cfnresponse.send(event, context, cfnresponse.FAILED, {"Message": error_message})
