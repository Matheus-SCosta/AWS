import boto3
import os
import logging
from logging import getLogger, StreamHandler, Formatter


ec2 = boto3.client('ec2', region_name='us-east-2')
sns = boto3.resource('sns', region_name='us-east-2')
topic_arn = sns.PlatformEndpoint('arn:aws:sns:us-east-2:398963803929:Start_Valida')



logger = getLogger()
handler = StreamHandler()
formatter = Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)


def publish_message_sns(topic_arn, message): 
    response = topic_arn.publish(Message=message)
    message_id = response['MessageId']
    logger.info('Message publish in topic SNS')
    

def check_availability():
    while True:
        response = ec2.describe_instance_status(InstanceIds=['i-032398d6054a962e1'])
        for key, value in response.items():
            if key == 'InstanceStatuses' and value:
                logger.info('ec2 i-032398d6054a962e1 initializing')
                for array in value:
                    for key, value in array.items():
                        if key == 'InstanceStatus': 
                            for key, value in value.items():
                                if key == 'Status': status = value
    
        if 'status' in locals() and status == 'ok': logger.info('ec2 i-032398d6054a962e1 available'); break
        else: logger.info('ec2 i-032398d6054a962e1 not available or initializing')
        os.system("sleep 10")                            
    

if __name__ == "__main__":
    publish_message_sns(topic_arn, "Starting Server Valida")
    check_availability()