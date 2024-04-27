import boto3
import cfnresponse
import os

# Create a Secrets Manager client
secretsmanager = boto3.client('secretsmanager')

import json

secret_name = "MyRDSCredentials"

def lambda_handler(event, context):
    try:
        username = event['ResourceProperties']['Username']
        password = event['ResourceProperties']['Password']
        db_endpoint = os.environ['DB_ENDPOINT']

        secret_string = json.dumps({
            'username': username,
            'password': password,
            'host': db_endpoint,
            'dbname': 'exampledb',
            'port': 3306
        })
        secretsmanager.create_secret(
            Name=secret_name,
            Description="RDS database credentials",
            SecretString=secret_string
        )
        # Prepare the response data
        response_data = {"Success": "Username and password parameters have been set successfully."}
        cfnresponse.send(event, context, cfnresponse.SUCCESS, response_data)
    except Exception as e:
        # Prepare the error message
        error_message = str(e)

        # Send failure response to CloudFormation
        cfnresponse.send(event, context, cfnresponse.FAILED, {"Message": error_message})
