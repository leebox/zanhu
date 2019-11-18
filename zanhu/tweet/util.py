# -*- coding:utf8 -*-
from django.shortcuts import render
from functools import wraps
from django.http import HttpResponseBadRequest
from django.views.generic import View
from django.core.exceptions import PermissionDenied


def ajax_required(f):
    """验证是否为ajax请求"""
    @wraps(f) # 不改变使用装饰器原有函数的结构(如__name__, __doc__)
    def wrap(request, *args, **kwargs):
        # request.is_ajax() 方法判断是否为Ajax请求
        if not request.is_ajax():
            return HttpResponseBadRequest("不是ajax请求!")
        return f(request, *args, **kwargs)

    return wrap


class AuthorRequireMixin(View):
    """
    验证是否为原作者, 用于状态，删除文章等
    """
    def dispatch(self, request, *args, **kwargs):
        if self.get_object().user.username != self.request.user.username:
            raise PermissionDenied
        return super().dispatch(request, *args, **kwargs)
