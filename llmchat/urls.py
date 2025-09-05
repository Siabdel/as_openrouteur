from django.urls import path
from . import views

urlpatterns = [
    path('', views.home_page, name='home'),  # New path for home page
]