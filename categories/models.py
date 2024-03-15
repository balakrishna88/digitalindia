from django.db import models

from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

from inf import settings




# Create your models here.
class EducationCategory(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class EducationSubCategory(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(EducationCategory, on_delete=models.CASCADE)
    subcategory = models.CharField(max_length=255, blank=True)  # Field to store the combined name

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.subcategory:  # If combined_name is not set, generate it
            self.subcategory = f"{self.category.name} - {self.name}"
        super().save(*args, **kwargs)




class Contact(models.Model):
    full_name = models.CharField(max_length=100)
    email = models.EmailField()
    phone = models.CharField(max_length=20)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f'{self.full_name} - {self.email}'
    



