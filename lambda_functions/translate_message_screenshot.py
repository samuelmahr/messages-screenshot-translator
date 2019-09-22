import base64
import logging.config
import json

import boto3


LOGGER = logging.getLogger()
LOGGER.setLevel(logging.INFO)
TEXTRACT_CLIENT = boto3.client('textract')
TRANSLATE_CLIENT = boto3.client('translate')


def handler(event, context):
    LOGGER.debug(json.dumps(event))
    if event.get('httpMethod'):
        return handle_http_request(event)

    if event.get('Records'):
        return handle_s3_request(event)


def handle_http_request(event):
    request_payload = json.loads(event['body'])
    image = base64.b64decode(request_payload['image'])
    source_language = request_payload['source_language']
    target_language = request_payload['target_language']
    message_dialogue = analyze_image_bytes(image)
    # translate_dialogue = translate_extracted_text(message_dialogue, source_language, target_language)
    return {
        'statusCode': 200,
        'body': json.dumps({'message': 'Request received, soon to be implemented'})
    }


def analyze_image_bytes(image_bytes):
    response = TEXTRACT_CLIENT.detect_document_text(
        Document={
            'Bytes': image_bytes
        }
    )

    for block in response['Blocks']:
        if block['BlockType'] == 'LINE':
            LOGGER.info(block)

    return list()


def handle_s3_request(event):
    return {'message': 'S3 event received, soon to be implemented'}
