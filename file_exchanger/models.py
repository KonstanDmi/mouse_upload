from django.db import models
from django import forms



# Create your models here.


class DirUploadModel(models.Model):
    id = models.IntegerField(primary_key=True,  editable=False)
    set_id = models.CharField(max_length=32, editable=False, unique=False, default='sdfghjkjhgfd')
    file = models.FileField(upload_to='mouse', verbose_name='File')
    timestamp = models.IntegerField()

    class Meta:
        verbose_name = "File"
        verbose_name_plural = "Files"
