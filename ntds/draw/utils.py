import string
import random
import requests
from requests_aws4auth import AWS4Auth
from ntds.settings import CF_UPLOAD_URL, CF_SECRET_ACCESS_KEY, CF_ACCESS_KEY, CF_REGION, CF_SERVICE
from django.http import JsonResponse

def generate_link(num, length=8):
    alphabet = string.digits + string.ascii_letters

    base = len(alphabet)
    encoded = []
    while num:
        num, rem = divmod(num, base)
        encoded.append(alphabet[rem])
    while len(encoded) < length:
        
        encoded.append(random.choice(alphabet))
    return ''.join(reversed(encoded))



class CF_ACCESS():
    def __init__(self):
        self.url = CF_UPLOAD_URL
        self.authorization = AWS4Auth(CF_ACCESS_KEY, CF_SECRET_ACCESS_KEY, CF_REGION, CF_SERVICE)

    def put(self, image):

        put_headers = {
            'Content-Type': image.content_type,
        }

        try:
            response = requests.put(
                self.url + image.name,
                data=image,
                headers=put_headers,
                auth=self.authorization,
            )

            if response.status_code != 200:
                return {'error': 'Failed to upload image'}, 500
            return {'message': 'Image uploaded'}, 200
        except requests.RequestException as e:
            print(f"RequestException: {e}")
            return {'error': 'Error while uploading image'}, 500
        
    
    def delete(self):
        pass


    