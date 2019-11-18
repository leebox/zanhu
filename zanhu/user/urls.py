# -*- coding:utf8 -*-
from django.urls import path
from . import views

app_name = 'user'

urlpatterns = [
    path('<username>/', views.UserDetail.as_view(), name='detail_page'),
    path('<username>/setting/', views.UserUpdateDetail.as_view(), name='setting_page'),

]
