import boto3
import json
from .config import settings

def get_sqs_client():
    return boto3.client(
        "sqs",
        region_name=settings.AWS_REGION
    )

def send_message_to_queue(message: dict):
    sqs = get_sqs_client()
    response = sqs.send_message(
        QueueUrl=settings.SQS_QUEUE_URL,
        MessageBody=json.dumps(message)
    )
    return response
