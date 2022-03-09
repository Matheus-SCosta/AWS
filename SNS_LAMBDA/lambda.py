from __future__ import print_function
import json
import boto3
import os
import sys


print('Loading function')


def lambda_handler(event, context):
    message = event['Records'][0]['Sns']['Message']
    if message == "Stopping Server Valida":
        print("Stopping Server Valida")
        stop_ec2(instances = ['i-032398d6054a962e1'])
    elif message == 'Starting Server Valida':
        print("Starting Server Valida")
        start_ec2(instances = ['i-032398d6054a962e1'])
    else:
        print("Invalid message")
        sys.exit()
    return message
    
    
def start_ec2(instances):
    print(f"Instance Starting {instances}")
    ec2 = boto3.client('ec2', region_name='us-east-2')
    ec2.start_instances(InstanceIds=instances)
    print('started your instances: ' + str(instances))


def stop_ec2(instances):
    print(f"Instance Stopping {instances}")
    ec2 = boto3.client('ec2', region_name='us-east-2')
    ec2.stop_instances(InstanceIds=instances)
    print('stopped your instances: ' + str(instances))
    
    
    
    
    
    