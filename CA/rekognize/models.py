from django.db import models

class Image(models.Model):
    image = models.ImageField(null=False, blank=False)
    description = models.TextField(default='')
    def __str__(self):
        return self.image.name
# Simple image model, for our purposes it does the job perfectly