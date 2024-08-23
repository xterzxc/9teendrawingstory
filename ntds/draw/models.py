from django.db import models

class Drawing(models.Model):
    # user = foreingkey
    title = models.CharField(max_length=100)
    description = models.CharField(max_length=200, null=True)
    likes = models.IntegerField(default=0)
    # comments = manytomanyfield
    created_at = models.DateTimeField(auto_now_add=True)
    imgname = models.CharField(max_length=64)
    imglink = models.URLField()

    def __str__(self):
        return self.title