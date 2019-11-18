
# -*- coding:utf8 -*-
from .models import Tweet
from django.views.generic import ListView, DeleteView
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_http_methods
from zanhu.tweet.util import ajax_required, AuthorRequireMixin
from django.shortcuts import render
from django.template.loader import render_to_string
from django.http import HttpResponseBadRequest, JsonResponse, HttpResponse
from django.urls import reverse_lazy


# Create your views here.
class TweetListView(LoginRequiredMixin, ListView):
    model = Tweet
    paginate_by = 20
    context_object_name = 'tweet_list'
    template_name = 'tweet/tweet_list.html'

    def get_queryset(self):
        return Tweet.objects.filter(reply=False)


@login_required
@ajax_required
@require_http_methods(['POST'])
def post_new_tweet(request):
    """发送动态，Ajax请求"""
    post_tweet = request.POST['content'].strip()
    if post_tweet:
        new_tweet = Tweet.objects.create(user=request.user, content=post_tweet)
        return render(request, template_name='tweet/single_tweet.html',
                      context={'tweet': new_tweet})
    else:
        return HttpResponseBadRequest('动态内容不能为空')


class TweetDeleteView(LoginRequiredMixin, AuthorRequireMixin, DeleteView):
    model = Tweet
    template_name = 'tweet/tweet_confirm_delete.html'
    slug_url_kwarg = 'slug'
    pk_url_kwarg = 'pk'
    success_url = reverse_lazy('tweet:index_page')


@login_required
@ajax_required
@require_http_methods(['POST'])
def add_like(request):
    """添加或删除点赞"""
    current_pk = request.POST['pk']
    if current_pk:
        current_tweet = Tweet.objects.get(pk=current_pk)
        current_tweet.switch_like(request.user)
        total_like = current_tweet.liked_user.count()
        return JsonResponse({'total_like': total_like})
    else:
        return HttpResponseBadRequest('当前PK值无效')


@login_required
@ajax_required
@require_http_methods(['GET'])
def get_comment_list(request):
    """GET请求方式获取评论"""
    current_pk = request.GET['pk']
    if current_pk:
        current_comments = Tweet.objects.filter(parent_id=current_pk)
        html = render_to_string("tweet/single_comment.html",
                                {"current_comments": current_comments})
        return JsonResponse({'html': html})
    else:
        return HttpResponseBadRequest('没有评论')


@login_required
@ajax_required
@require_http_methods(['POST'])
def post_new_comment(request):
    """发送动态，Ajax请求"""
    post_parent_id = request.POST['parent_id'].strip()
    post_content = request.POST['content'].strip()
    new_comment = Tweet.objects.create(user=request.user, content=post_content,
                                       parent_id=post_parent_id, reply=True)
    return HttpResponse('OK')
