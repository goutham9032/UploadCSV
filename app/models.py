from django.db import models

class UploadCsv(models.Model):
    name = models.CharField(max_length=255, blank=True)
    sku = models.CharField(max_length=255, unique=True)
    description = models.TextField(max_length=10000)

    def __str__(self):
        return self.sku


