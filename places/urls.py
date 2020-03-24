from django.urls import path
from . import views

urlpatterns = [
    path('<pk>', views.index, name='index'),
]