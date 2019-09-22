import base64

import requests


def test_post_image():
    with open('images/test_screenshot.png', 'rb') as image:
        payload = {
            'source_language': 'en',
            'target_language': 'fr',
            'image': base64.b64encode(image.read()).decode('ascii')
        }

        response = requests.post('https://l7xhep2en7.execute-api.us-east-1.amazonaws.com/funsies/message/translate',
                                 json=payload,
                                 headers={'isBase64Encoded': 'true'})

        print(response.text)
        response.raise_for_status()
