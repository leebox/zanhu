from django.shortcuts import render
from django.views.generic import CreateView, ListView, DetailView, UpdateView, DeleteView
from .models import Post
from .helper import increase_page_view, save_draft_redis
from django.urls import reverse
from django.contrib.auth.mixins import LoginRequiredMixin
from django.http import JsonResponse, HttpResponse


# Create your views here.
class AddPost(LoginRequiredMixin, CreateView):
    template_name = 'post/add.html'
    model = Post
    fields = ['title', 'content']
    success_url = '/post/list'

    def form_valid(self, form):
        if self.request.is_ajax():
            # ajax 保存文章草稿
            draft = save_draft_redis(self.request.user.pk,
                                     form.cleaned_data['title'],
                                     form.cleaned_data['content'])
            return JsonResponse(draft)
        else:
            f = form.save(commit=False)  # 传过来的form data不要保存
            f.author_id = self.request.user.pk  # 添加一个作者字段
            f.save()  # 保存form data
            response = super().form_valid(form)
            return response

    def form_invalid(self, form):
        response = super().form_invalid(form)
        if self.request.is_ajax():
            return JsonResponse(form.errors, status=400)
        return response


class DraftListView(ListView):
    template_name = 'post/drafts_list.html'
    model = Post
    context_object_name = 'draft_post_list'

    def get_queryset(self):
        return Post.objects.filter(author=self.request.user, status='D').order_by('-created')


class PostList(ListView):
    template_name = 'post/list.html'
    model = Post
    context_object_name = 'post_list'


class UpdatePost(LoginRequiredMixin, UpdateView):
    template_name = 'post/update.html'
    model = Post
    fields = ['title', 'content']

    def get_success_url(self):
        return reverse('post:post_detail', kwargs={'pk': self.kwargs['pk']})


class PostDetail(DetailView):
    template_name = 'post/detail.html'
    model = Post

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cache_view_num'] = increase_page_view(context['object'].pk)
        return context


class DeletePostView(DeleteView):
    model = Post
    success_url = '/post/list'

    def post(self, request, *args, **kwargs):
        if self.request.is_ajax():
            Post.objects.filter(id=self.request.POST['pk']).delete()
            return HttpResponse(status=200)
        return super().post(request, *args, **kwargs)