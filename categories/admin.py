from django.contrib import admin

# Register your models here.
from django.contrib import admin
from .models import EducationCategory, EducationSubCategory
from .models import Contact

# Register your models here.

@admin.register(EducationCategory)
class EducationCategoryAdmin(admin.ModelAdmin):
    list_display = ('name',)

@admin.register(EducationSubCategory)
class EducationSubCategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'category', 'subcategory')
    list_filter = ('category',)
    search_fields = ('name', 'category__name')

admin.site.register(Contact)

