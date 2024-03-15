from django.shortcuts import get_object_or_404, render
from categories.models import EducationCategory, EducationSubCategory
from education.models import EducationPost, Tag
from django.contrib.auth.decorators import login_required

def home(request):
    
    education_posts = EducationPost.objects.all().order_by('-created_at')
    random_posts = EducationPost.objects.all().order_by('?')[:5]
    return render(request, 'home.html', {'education_posts': education_posts,'random_posts':random_posts})

def contact(request):
    return render(request, 'contact.html')





def search(request):
    query = request.GET.get('query')
    if query:
        education_posts = EducationPost.objects.filter(title__icontains=query)
        categories = EducationCategory.objects.filter(name__icontains=query)
        subcategories = EducationSubCategory.objects.filter(name__icontains=query)
        tags = Tag.objects.filter(name__icontains=query)
        context = {
            'education_posts': education_posts,
            'categories': categories,
            'subcategories': subcategories,
            'tags': tags,
            'query': query,
        }
        return render(request, 'search.html', context)
    else:
        # Handle case where no query is provided
        return render(request, 'search.html')
    


@login_required
def mydashboard(request):
    return render(request, 'dashboard.html')


