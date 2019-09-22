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
    translated_dialogue = translate_extracted_text(message_dialogue, source_language, target_language)
    return {
        'statusCode': 200,
        'body': json.dumps({'dialogue': translated_dialogue}, ensure_ascii=False)
    }


def analyze_image_bytes(image_bytes):
    response = TEXTRACT_CLIENT.detect_document_text(
        Document={
            'Bytes': image_bytes
        }
    )

    is_first = True
    is_last_speaker_person = False
    speaker_text = ''
    dialogue = list()
    for block in response['Blocks']:
        is_speaker_person = bool(0.07 < block['Geometry']['BoundingBox']['Left'] < 0.08)
        if is_first:
            is_last_speaker_person = is_speaker_person
            is_first = False

        if block['BlockType'] == 'LINE':
            if is_last_speaker_person and not is_speaker_person and speaker_text:
                dialogue.append(f'Person: {speaker_text}')
                speaker_text = f"{block['Text']} "
            elif not is_last_speaker_person and is_speaker_person and speaker_text:
                dialogue.append(f'You: {speaker_text}')
                speaker_text = f"{block['Text']} "
            elif is_speaker_person == is_last_speaker_person:
                speaker_text += f"{block['Text']} "

            is_last_speaker_person = is_speaker_person

    return dialogue


def translate_extracted_text(message_dialogue, source_language, target_language):
    translated_dialogue = list()
    for message in message_dialogue:
        response = TRANSLATE_CLIENT.translate_text(
            Text=message,
            SourceLanguageCode=source_language,
            TargetLanguageCode=target_language
        )
        translated_dialogue.append(response['TranslatedText'].encode('utf-8').decode())
        LOGGER.info(response['TranslatedText'])

    return translated_dialogue


def handle_s3_request(event):
    return {'message': 'S3 event received, soon to be implemented'}
