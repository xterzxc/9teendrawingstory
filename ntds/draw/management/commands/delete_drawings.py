from django.contrib.auth import get_user_model
from draw.models import Drawing
from faker import Faker
import random
import os
from django.core.management.base import BaseCommand
from ntds.utils import CF_ACCESS

# flag users чтобы удалять юзеров
class Command(BaseCommand):
    help = 'Delete all Drawing objects from the database and non admin users'

    def handle(self, *args, **kwargs):
        drawings = Drawing.objects.all()
        drawings_count = drawings.count()



        if drawings_count == 0:
            self.stdout.write(self.style.WARNING('No drawings found to delete.'))
            return


        cf_access = CF_ACCESS()
        for drawing in drawings:
            cf_delete, status_code = cf_access.delete(drawing.imgname)
            if status_code != 200:
                self.stdout.write(self.style.ERROR(f"Failed to delete drawing {drawing}"))
                continue

            if not drawing.owner.is_superuser:  
                drawing.owner.delete()
            drawing.delete()
            self.stdout.write(self.style.SUCCESS(f'Deleted drawing {drawing.title} and user {drawing.owner}'))

        self.stdout.write(self.style.SUCCESS(f'Success deleted {drawings_count} drawings.'))