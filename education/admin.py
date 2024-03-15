from django.contrib import admin

from education.models import EducationPost, Tag
from django_summernote.admin import SummernoteModelAdmin
# Register your models here.


# Register your models here.

from django.contrib import admin
from .models import EducationPost, Tag

class TagInline(admin.TabularInline):
    model = EducationPost.tags.through
    extra = 1
    readonly_fields = ['get_tag_name']

    def get_tag_name(self, instance):
        return instance.tag.name


@admin.register(EducationPost)
class EducationPostAdmin(SummernoteModelAdmin):
    list_display = ('title', 'category', 'subcategory', 'created_at', 'modified_at')
    list_filter = ('category', 'subcategory')
    search_fields = ('title', 'content', 'category__name', 'subcategory__name')
    prepopulated_fields = {'slug': ('title',)}
    readonly_fields = ('created_at', 'modified_at')
    inlines = [TagInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if 'tags' in form.base_fields:
            del form.base_fields['tags']
        return form

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name',)  # Display the 'name' field in the list view
