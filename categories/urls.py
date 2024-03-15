from django.urls import path
from . import views

urlpatterns = [
    # Other URL patterns...
    path('contact_form/', views.contact_form, name='contact_form'),
    
    
]
