from django.test import TestCase, Client
from django.urls import reverse
from unittest.mock import patch
from .models import Drawing
from io import BytesIO
from ntds.settings import CF_GET_URL
from PIL import Image

class DrawingCreateViewTest(TestCase):
    
    def setUp(self):
        self.client = Client()
        self.url = reverse('draw-create')

    def test_no_image_provided(self):
        response = self.client.post(self.url, {
            'title': 'Test title',
            'description': 'Test description',
        })
        self.assertEqual(response.status_code, 400)
        self.assertEqual(response.json()['error'], 'No image provided')

    @patch('draw.utils.CF_ACCESS.put')
    def success_test_upload_image(self, mock_cf_access_put):
        img = BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(img, format='PNG')
        img.seek(0)
        img.name = 'test_image.png'

        mock_cf_access_put.return_value = ({}, 200)

        response = self.client.post(self.url, {
            'title': 'Test title',
            'description': 'Test description',
            'image': img
        })

        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.json()['message'], 'Image')
        
        drawing = Drawing.objects.last()
        self.assertTrue(drawing)
        self.assertTrue(drawing.imgname)
        self.assertTrue(drawing.imglink.startswith(CF_GET_URL))

    @patch('draw.utils.CF_ACCESS.put')
    def error_test_upload_image(self, mock_cf_access_put):
        img = BytesIO()
        image = Image.new('RGB', (100, 100))
        image.save(img, format='PNG')
        img.seek(0)
        img.name = 'test_image.png'

        mock_cf_access_put.return_value = ({'error': 'Upload failed'}, 500)

        response = self.client.post(self.url, {
            'title': 'Test title',
            'description': 'Test description',
            'image': img
        })

        self.assertEqual(response.status_code, 500)
        self.assertEqual(response.json()['error'], 'Upload failed')
