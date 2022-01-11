from django.db import models

class ZIP(models.Model):
    name = models.CharField(max_length=50)
    ZIPFILE = models.FileField(upload_to='zipfiles/')