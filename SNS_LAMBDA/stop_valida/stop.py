import boto3
import os
import random
sns = boto3.resource('sns', region_name='us-east-2')
topic_arn = sns.PlatformEndpoint('arn:aws:sns:us-east-2:398963803929:Stop_valida')


def test_app():
    while True:
        num = random.randint(0, 10)
        if num == 0:
            print('Build Sucess')
            publish_message(topic_arn, "Stopping Server Valida")
            break
        print('Build Failed')
        os.system("sleep 30")


def publish_message(topic_arn, message): 
    response = topic_arn.publish(Message=message)
    message_id = response['MessageId']
    print(response, message_id)

if __name__ == "__main__":
    test_app()