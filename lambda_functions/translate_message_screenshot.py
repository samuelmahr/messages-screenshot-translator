import logging.config
import json

import boto3
from PIL import Image


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)


def handler(event, context):
    if event.get('httpMethod'):
        return handle_http_request(event)

    if event.get('Records'):
        return handle_s3_request(event)


def handle_http_request(event):
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Request received, soon to be implemented'})
    }


def handle_s3_request(event):
    return {'message': 'S3 event received, soon to be implemented'}
