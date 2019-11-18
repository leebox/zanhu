# -*- coding:utf8 -*-
from django.urls import path
from . import views

app_name = 'tweet'

urlpatterns = [
    path('', views.TweetListView.as_view(), name="index_page"),
    path('post_new_tweet', views.post_new_tweet, name='post_new_tweet'),
    path('delete/<str:pk>', views.TweetDeleteView.as_view(), name='delete_tweet'),
    path('like/', views.add_like, name='like_tweet'),
    path('comment/list/', views.get_comment_list, name='comment_list'),
    path('post_new_comment/', views.post_new_comment, name='post_new_comment'),
]
