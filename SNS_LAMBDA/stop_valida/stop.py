import boto3
import os
import random
import logging
from logging import getLogger, StreamHandler, Formatter

logger = getLogger()
handler = StreamHandler()
formatter = Formatter('%(asctime)s %(name)-12s %(levelname)-8s %(message)s')
handler.setFormatter(formatter)
logger.addHandler(handler)
logger.setLevel(logging.DEBUG)

sns = boto3.resource('sns', region_name='us-east-2')
topic_arn = sns.PlatformEndpoint('arn:aws:sns:us-east-2:398963803929:Stop_valida')



def publish_message(topic_arn, message): 
    response = topic_arn.publish(Message=message)
    message_id = response['MessageId']
    print(response, message_id)
    logger.info('Message publish in topic SNS')


if __name__ == "__main__":
    publish_message(topic_arn, "Stopping Server Valida")