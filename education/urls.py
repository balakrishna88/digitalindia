from django.urls import path
from . import views

urlpatterns = [
    path('create/', views.create_education_post, name='create_education_post'),
    path('success/', views.education_success, name='education_success'),

    # path('education/', views.education_posts, name='education_posts'),
    # path('education/<int:post_id>/', views.education_details, name='education_details'),

    # path('education_categories/<int:category_id>/', views.education_category_detail, name='education_category_detail'),
     
    # path('education_subcategory/<int:subcategory_id>/', views.subcategory_detail, name='subcategory_detail'),




    path('education/', views.education, name='education'),
     path('education/<str:category_name>/', views.category_detail, name='category_detail'),
    path('education/post/<slug:post_slug>/', views.post_detail, name='post_detail'),

    path('education/<str:category_name>/<str:subcategory_name>/', views.subcategory_detail, name='subcategory_detail'),

    

    path('tag/<str:tag_name>/', views.posts_by_tag, name='posts_by_tag'),
    path('post/<slug:post_slug>/', views.post_detail, name='post_detail'),

    
    
]
