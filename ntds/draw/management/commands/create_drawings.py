import os
import uuid
import mimetypes
from django.contrib.auth import get_user_model
from draw.models import Drawing
from faker import Faker
import random
from ntds.utils import CF_ACCESS
from ntds.settings import CF_GET_URL
from django.core.management.base import BaseCommand
from draw.utils import generate_link

FOLDER = 'static/images/drawings/'
User = get_user_model()

class Command(BaseCommand):
    help = 'Creating N users with N drawings'

    def add_arguments(self, parser):
        parser.add_argument('users', type=int, help='Number of users to create')
        parser.add_argument('drawings', type=int, help='Number of drawings to create per user')

    def handle(self, *args, **kwargs):
        users = kwargs['users']
        drawings = kwargs['drawings']
        fake = Faker()

        images = [f for f in os.listdir(FOLDER) if os.path.isfile(os.path.join(FOLDER, f))]
        images_backup = images.copy()

        if not images:
            self.stdout.write(self.style.ERROR(f'Folder {FOLDER} is empty'))
            return

        for _ in range(users):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123'
            )
            self.stdout.write(self.style.SUCCESS(f'User: {user.username} created'))

            for _ in range(drawings):
                if len(images) == 0:
                    images = images_backup.copy()

                random_image = random.choice(images)
                images.remove(random_image)
                image_uuid = str(uuid.uuid4())
                image_link = CF_GET_URL + image_uuid

                class UploadedFileWrapper:
                    def __init__(self, file, name, content_type):
                        self.file = file
                        self.name = name
                        self.content_type = content_type

                    def read(self):
                        return self.file.read()

                image_path = os.path.join(FOLDER, random_image)
                with open(image_path, 'rb') as image_file:
                    content_type, _ = mimetypes.guess_type(image_path)
                    if content_type is None:
                        content_type = 'application/octet-stream'

                    wrapped_image = UploadedFileWrapper(image_file, image_uuid, content_type)

                    cf_access = CF_ACCESS()
                    cf_upload, status_code = cf_access.put(wrapped_image)

                    if status_code != 200:
                        self.stdout.write(self.style.ERROR(f"Failed to upload image {random_image}"))
                        continue

                drawing = Drawing.objects.create(
                    owner=user,
                    title=fake.sentence(nb_words=3),
                    description=fake.text(max_nb_chars=100),
                    likes=random.randint(0, 100),
                    imgname=image_uuid,
                    imglink=image_link,
                )
                self.stdout.write(self.style.SUCCESS(f'Created drawing: {drawing.title} for user {user.username}'))

        self.stdout.write(self.style.SUCCESS(f'Successfully created {users} users with {drawings} drawings each'))
