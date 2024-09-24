import requests
from requests_aws4auth import AWS4Auth
from ntds.settings import CF_UPLOAD_URL, CF_SECRET_ACCESS_KEY, CF_ACCESS_KEY, CF_REGION, CF_SERVICE


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
        
    
    def delete(self, image):


        try:
            response = requests.delete(
                self.url + image,
                data=image,
                auth=self.authorization,
            )

            if response.status_code != 204:
                return {'error': 'Failed to delete image'}, 500
            return {'message': 'Image deleted'}, 200
        except requests.RequestException as e:
            print(f"RequestException: {e}")
            return {'error': 'Error while deleting image'}, 500