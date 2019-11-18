from django.db import models
from django.conf import settings
# Create your models here.
from froala_editor.fields import FroalaField
from django.contrib.contenttypes.fields import GenericRelation
from zanhu.comment.models import Comment


class Post(models.Model):
    """文章模型"""
    STATUS_CHOICES = (('D', '草稿'), ('P', '发表'),)
    title = models.CharField(max_length=255, verbose_name='标题')
    content = FroalaField(verbose_name='内容', blank=True, null=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES, default='p')
    author = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
                               verbose_name='作者')
    view_num = models.PositiveIntegerField(default=0, verbose_name='浏览次数')
    category = models.ForeignKey('Category', verbose_name='分类', on_delete=models.PROTECT, blank=True, null=True)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合')
    comments = GenericRelation(Comment)

    class Meta:
        verbose_name = "文章"
        verbose_name_plural = verbose_name
        ordering = ['-created']

    def __str__(self):
        return self.title


class Category(models.Model):
    """文章分类"""
    name = models.CharField(verbose_name='分类名', max_length=10, unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "分类"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name


class Tag(models.Model):
    """文章标签"""
    name = models.CharField(verbose_name='标签名', max_length=10, unique=True)
    created = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = "标签"
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name
