from django.contrib.auth import get_user_model
from draw.models import Drawing
from faker import Faker
import random
import os
from django.core.management.base import BaseCommand


FOLDER = 'static/images/drawings/'
User = get_user_model()

class Command(BaseCommand):
    help = 'Creating N users with N drawings'

    def add_arguments(self, parser):
        parser.add_argument('users', type=int, help='users to create')
        parser.add_argument('drawings', type=int, help='d1rawings to create per user')

    def handle(self, *args, **kwargs):
        users = kwargs['users']
        drawings = kwargs['drawings']
        

        fake = Faker()

        images = [f for f in os.listdir(FOLDER) if os.path.isfile(os.path.join(FOLDER, f))]

        if not images:
            self.stdout.write(self.style.ERROR(f'Folder {FOLDER} empty'))
            return


        for _ in range(users):
            user = User.objects.create_user(
                username=fake.user_name(),
                email=fake.email(),
                password='password123'
            )
            self.stdout.write(self.style.SUCCESS(f'User: {user.username}'))

            for _ in range(drawings):
                random_image = random.choice(images)
                image_link = os.path.join(FOLDER, random_image)
                images.remove(random_image)
                drawing = Drawing.objects.create(
                    owner=user,
                    title=fake.sentence(nb_words=3),
                    description=fake.text(max_nb_chars=100),
                    likes=random.randint(0, 100),
                    imgname=random_image,
                    imglink=image_link,
                )
                self.stdout.write(self.style.SUCCESS(f'Created drawing: {drawing.title} for user {user.username}'))

        self.stdout.write(self.style.SUCCESS(f'Success {users} {drawings}'))