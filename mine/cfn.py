"""
This lambda implements the custom resource handler for creating an SSH key
and storing in in SSM parameter store.

e.g.

SSHKeyCR:
    Type: Custom::CreateSSHKey
    Version: "1.0"
    Properties:
      ServiceToken: !Ref FunctionArn
      KeyName: MyKey

An SSH key called MyKey will be created.
"""

from json import dumps
import sys
import traceback
import urllib.request
import boto3
from botocore.exceptions import ClientError
import json


def log_exception():
    """Log a stack trace"""
    exc_type, exc_value, exc_traceback = sys.exc_info()
    print(repr(traceback.format_exception(
        exc_type,
        exc_value,
        exc_traceback)))


def send_response(event, context, response):
    """Send a response to CloudFormation to handle the custom resource lifecycle"""
    response_body = {
        'Status': response,
        'Reason': 'See details in CloudWatch Log Stream: ' + \
            context.log_stream_name,
        'PhysicalResourceId': context.log_stream_name,
        'StackId': event['StackId'],
        'RequestId': event['RequestId'],
        'LogicalResourceId': event['LogicalResourceId'],
    }
    print('RESPONSE BODY: \n' + dumps(response_body))
    data = dumps(response_body).encode('utf-8')
    req = urllib.request.Request(
        event['ResponseURL'],
        data,
        headers={'Content-Length': len(data), 'Content-Type': ''})
    req.get_method = lambda: 'PUT'
    try:
        with urllib.request.urlopen(req) as resp:
            print(f'response.status: {resp.status}, ' +
                  f'response.reason: {resp.reason}')
            print('response from cfn: ' + resp.read().decode('utf-8'))
    except urllib.error.URLError:
        log_exception()
        raise Exception('Received non-200 response while sending response to AWS CloudFormation')
    return True

import boto3
from botocore.exceptions import ClientError
import json

def custom_resource_handler(event, context):
    print("Event JSON: \n" + json.dumps(event))
    pem_key_name = event['ResourceProperties']['KeyName']
    ec2 = boto3.client('ec2')
    ssm = boto3.client('ssm')
    response = 'FAILED'

    if event['RequestType'] == 'Create':
        try:
            # Check for key existence in EC2 and SSM
            try:
                ec2.describe_key_pairs(KeyNames=[pem_key_name])
                key_exists_in_ec2 = True
            except ClientError as e:
                if 'InvalidKeyPair.NotFound' in str(e):
                    key_exists_in_ec2 = False
                else:
                    print(f"Error checking key pair: {e}")
                    raise

            try:
                ssm.get_parameter(Name=pem_key_name, WithDecryption=False)
                key_exists_in_ssm = True
            except ClientError as e:
                if 'ParameterNotFound' in str(e):
                    key_exists_in_ssm = False
                else:
                    print(f"Error checking SSM parameter: {e}")
                    raise

            if not key_exists_in_ec2 and not key_exists_in_ssm:
                # Key does not exist in both EC2 and SSM, create new key pair
                key = ec2.create_key_pair(KeyName=pem_key_name)
                key_material = key['KeyMaterial']
                # Store the key in SSM Parameter Store
                ssm.put_parameter(
                    Name=pem_key_name,
                    Value=key_material,
                    Type='SecureString',
                    Overwrite=True
                )
                print(f"The parameter {pem_key_name} has been created.")
                response = 'SUCCESS'
            elif key_exists_in_ec2 and not key_exists_in_ssm:
                # Key exists in EC2 but not in SSM, handle accordingly
                print(f"Key {pem_key_name} exists in EC2 but not in SSM, cannot retrieve key material to store.")
                response = 'FAILED'
        except Exception as e:
            print(f'There was an error {e} creating and committing key {pem_key_name} to the parameter store')
            log_exception()
            response = 'FAILED'
        send_response(event, context, response)
        return

    if event['RequestType'] == 'Update':
        # Do nothing and send a success immediately
        send_response(event, context, 'SUCCESS')
        return

    if event['RequestType'] == 'Delete':
        try:
            # Delete the key from EC2 and SSM
            if ssm.delete_parameter(Name=pem_key_name):
                print(f"Deleted parameter {pem_key_name} from SSM.")
            if ec2.delete_key_pair(KeyName=pem_key_name):
                print(f"Deleted key pair {pem_key_name} from EC2.")
            response = 'SUCCESS'
        except Exception as e:
            print(f"There was an error {e} deleting the key {pem_key_name}")
            log_exception()
            response = 'FAILED'
        send_response(event, context, response)


def lambda_handler(event, context):
    """Lambda handler for the custom resource"""
    try:
        return custom_resource_handler(event, context)
    except Exception:
        log_exception()
        raise