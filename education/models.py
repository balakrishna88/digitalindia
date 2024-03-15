from django.db import models
from django.utils import timezone
from django.utils.text import slugify

from accounts.models import Account
from categories.models import EducationCategory, EducationSubCategory
  # Import your custom Account model

# models.py

from django.db import models
from django.utils import timezone
from django.utils.text import slugify

class Tag(models.Model):
    name = models.CharField(max_length=50)

    def __str__(self):
        return self.name

class EducationPost(models.Model):
    title = models.CharField(max_length=100)
    category = models.ForeignKey(EducationCategory, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(EducationSubCategory, on_delete=models.CASCADE)
    slug = models.SlugField(unique=True, blank=True)
    created_at = models.DateTimeField(default=timezone.now, editable=False)
    modified_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(Account, on_delete=models.CASCADE)
    content = models.TextField()
    tags = models.ManyToManyField(Tag)  # Many-to-Many relationship with Tag

    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        if not self.pk:  # If the post is being created for the first time
            self.created_at = timezone.now()
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
