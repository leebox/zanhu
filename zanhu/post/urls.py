# -*- coding:utf8 -*-

from django.urls import path

from . import views

app_name = 'post'


urlpatterns = [
    path('add/', views.AddPost.as_view(), name='add_post'),
    path('<int:pk>/update/', views.UpdatePost.as_view(), name='update_post'),
    path('list', views.PostList.as_view(), name='post_list'),
    path('<int:pk>/', views.PostDetail.as_view(), name='post_detail'),
    path('drafts/', views.DraftListView.as_view(), name='draft_list'),
    path('delete/', views.DeletePostView.as_view(), name='delete_post'),
]