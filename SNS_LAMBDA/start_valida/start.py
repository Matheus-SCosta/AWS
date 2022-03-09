import boto3
import os
import random
sns = boto3.resource('sns', region_name='us-east-2')
topic_arn = sns.PlatformEndpoint('arn:aws:sns:us-east-2:398963803929:Start_Valida')



def publish_message(topic_arn, message): 
    response = topic_arn.publish(Message=message)
    message_id = response['MessageId']
    print(response, message_id)

if __name__ == "__main__":
    publish_message(topic_arn, "Starting Server Valida")