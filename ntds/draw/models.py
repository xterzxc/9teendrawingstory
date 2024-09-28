from django.db import models
from users.models import User
from .utils import generate_link

class Drawing(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True)
    likes = models.IntegerField(default=0)
    pagelink = models.CharField(max_length=8, blank=True)
    # comments = manytomanyfield
    created_at = models.DateTimeField(auto_now_add=True)
    imgname = models.CharField(max_length=64)
    imglink = models.URLField()



    def save(self, *args, **kwargs):
        # Проверяем, есть ли у объекта уже ID (pk)
        if not self.pk:  # Первое сохранение объекта, когда ID ещё нет
            super().save(*args, **kwargs)  # Сохраняем объект для генерации ID
            self.pagelink = generate_link(self.id)  # Генерируем ссылку на основе ID
            # Второй раз сохраняем только с полем pagelink
            super().save(update_fields=['pagelink'])  # Сохраняем только поле pagelink
        else:
            super().save(*args, **kwargs)

    def __str__(self):
        return self.title
