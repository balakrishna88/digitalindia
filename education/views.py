from django.shortcuts import get_object_or_404, render
from django.shortcuts import render, redirect

from categories.models import EducationCategory, EducationSubCategory
from .forms import EducationPostForm
from categories.models import EducationCategory, EducationSubCategory
from .models import EducationPost, Tag
from django.shortcuts import render, redirect
from .forms import EducationPostForm
from django.utils.text import slugify
from django.views.generic import DetailView

from django.http import JsonResponse
from django.views.decorators.http import require_POST

from django.contrib import messages
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger




def create_education_post(request):
    if request.method == 'POST':
        form = EducationPostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.user = request.user  # Assign the current user to the user field
            slug = slugify(post.title)
            # Check if a post with the same slug exists
            if EducationPost.objects.filter(slug=slug).exists():
                # Append a number to the slug to make it unique
                count = 1
                while EducationPost.objects.filter(slug=f"{slug}-{count}").exists():
                    count += 1
                slug = f"{slug}-{count}"
            post.slug = slug
            post.save()
            messages.success(request, 'Post created successfully.')  # Add success message
            return redirect('create_education_post')  # Redirect to the same page after form submission
    else:
        form = EducationPostForm()
        categories = EducationCategory.objects.all()
        subcategories = EducationSubCategory.objects.all()
    return render(request, 'education/education_post.html', {'form': form, 'categories': categories, 'subcategories': subcategories})


def education_success(request):
    return render(request, 'education/education_success.html')





def education_posts(request):
    categories = EducationCategory.objects.all()
    # Fetch all education posts ordered by the 'created_at' field in descending order (newest first)
    education_posts = EducationPost.objects.all().order_by('-created_at')
    return render(request, 'education/education.html', {'categories': categories, 'education_posts': education_posts})

# def education_details(request, post_id):
#     post = get_object_or_404(EducationPost, pk=post_id)
#     return render(request, 'education/education_details.html', {'post': post})

# #-- education categories

# def education_category_detail(request, category_id):
#     category = EducationCategory.objects.get(id=category_id)
#     subcategories = EducationSubCategory.objects.filter(category=category)
#     return render(request, 'education/education_category_detail.html', {'category': category, 'subcategories': subcategories})



# def subcategory_detail(request, subcategory_id):
#     subcategory = get_object_or_404(EducationSubCategory, id=subcategory_id)
#     posts = EducationPost.objects.filter(subcategory=subcategory).order_by('-created_at')
#     return render(request, 'education/education_sub_category_detail.html', {'subcategory': subcategory, 'posts': posts})





def education(request):
    category = EducationCategory.objects.all().order_by('name')
    education_posts = EducationPost.objects.all().order_by('-created_at')
    subcategory = EducationSubCategory.objects.all()  # Fetch subcategories
    popular_posts = EducationPost.objects.all().order_by('?')[:5]
    all_tags = Tag.objects.all()
    # Pagination
    paginator = Paginator(education_posts, 3)  # Show 10 posts per page
    page = request.GET.get('page')
    try:
        education_posts = paginator.page(page)
    except PageNotAnInteger:
        # If page is not an integer, deliver first page.
        education_posts = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        education_posts = paginator.page(paginator.num_pages)

    return render(request, 'education/education.html', {'category': category, 'education_posts': education_posts, 'subcategory': subcategory, 'popular_posts': popular_posts, 'all_tags': all_tags})


def category_detail(request, category_name):
    category = get_object_or_404(EducationCategory, name=category_name)
    education_posts = EducationPost.objects.filter(category=category).order_by('-created_at')
    popular_posts = EducationPost.objects.all().order_by('?')[:5]
    cat_category = EducationCategory.objects.all().order_by('name')
    cat_subcategory = EducationSubCategory.objects.all()
    all_tags = Tag.objects.all()
    return render(request, 'education/category_detail.html', {'category': category, 'education_posts': education_posts, 'popular_posts': popular_posts, 'cat_category': cat_category,'cat_subcategory':cat_subcategory, 'all_tags': all_tags})

def subcategory_detail(request, category_name, subcategory_name):
    category = get_object_or_404(EducationCategory, name=category_name)
    subcategory = get_object_or_404(EducationSubCategory, name=subcategory_name)
    popular_posts = EducationPost.objects.all().order_by('?')[:5]
    posts = EducationPost.objects.filter(subcategory=subcategory)
    subcat_category = EducationCategory.objects.all().order_by('name')
    subcat_subcategory = EducationSubCategory.objects.all()
    all_tags = Tag.objects.all()
    return render(request, 'education/subcategory_detail.html', {'category': category, 'subcategory': subcategory, 'posts': posts, 'popular_posts': popular_posts, 'subcat_category': subcat_category,'subcat_subcategory':subcat_subcategory, 'all_tags': all_tags})

def post_detail(request, post_slug):
    post = get_object_or_404(EducationPost, slug=post_slug)
    popular_posts = EducationPost.objects.all().order_by('?')[:5]
    category = EducationCategory.objects.all().order_by('name')
    subcategory = EducationSubCategory.objects.all()  # Fetch subcategories
    all_tags = Tag.objects.all()
    return render(request, 'education/post_detail.html', {'post': post, 'popular_posts': popular_posts, 'category': category,'subcategory':subcategory, 'all_tags': all_tags})

def posts_by_tag(request, tag_name):
    category = EducationCategory.objects.all().order_by('name')
    education_posts = EducationPost.objects.all().order_by('-created_at')
    subcategory = EducationSubCategory.objects.all()  # Fetch subcategories
    popular_posts = EducationPost.objects.all().order_by('?')[:5]
    all_tags = Tag.objects.all()
    tag = Tag.objects.get(name=tag_name)
    education_posts = EducationPost.objects.filter(tags=tag)
    return render(request, 'education/tags.html', {'education_posts': education_posts, 'tag': tag,'category': category, 'education_posts': education_posts,'subcategory':subcategory, 'popular_posts': popular_posts, 'all_tags': all_tags})




