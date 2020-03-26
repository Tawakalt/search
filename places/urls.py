from django.urls import path, re_path
from .views import index, others

urlpatterns = [
    path('', index, name='index'),
    re_path(r'$', others, name='others'),
]