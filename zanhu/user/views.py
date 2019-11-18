# -*- coding:utf8 -*-
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic import UpdateView
from django.views.generic import DetailView
from .models import User


# Create your views here.
class UserDetail(LoginRequiredMixin, DetailView):
    model = User
    template_name = 'user/detail.html'
    slug_field = 'username'
    slug_url_kwarg = slug_field


class UserUpdateDetail(LoginRequiredMixin, UpdateView):
    model = User
    template_name = 'user/setting.html'
    slug_field = 'username'
    slug_url_kwarg = slug_field
    fields = ['gender', 'picture', 'introduction', 'location']

    def get_success_url(self):
        """更新成功后跳转到用户自己页面"""
        return reverse('user:setting_page', kwargs={'username': self.request.user.username})