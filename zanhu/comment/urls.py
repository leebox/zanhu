from django.urls import path
from . import views

app_name = 'comment'

urlpatterns = [
    path('', views.index, name='comment_index'),
]