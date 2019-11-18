# -*- coding:utf8 -*-
from django.db import models
import uuid
from django.conf import settings


# Create your models here.
class Tweet(models.Model):
    # uuid4 随机数生成
    uuid_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    # 发推的作者
    user = models.ForeignKey(settings.AUTH_USER_MODEL, blank=True, null=True, on_delete=models.SET_NULL,
                             related_name='publisher', verbose_name='用户')
    # 主推文，但reply为false时，自身就为评论
    parent = models.ForeignKey('self', blank=True, null=True, on_delete=models.CASCADE, related_name="thread",
                               verbose_name='自关联')
    # 推文或评论推文中的内容
    content = models.TextField(verbose_name='动态内容')
    # reply为TRUE就为推文的评论
    reply = models.BooleanField(default=False, verbose_name='是否为评论')
    # 点赞的用户，一条推文可以有很多赞，用户也可以点赞多个推文
    liked_user = models.ManyToManyField(settings.AUTH_USER_MODEL, verbose_name='点赞用户',
                                        related_name='liked_user')
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='创建时间')
    updated_at = models.DateTimeField(auto_now=True, verbose_name='更新时间')

    class Meta:
        verbose_name = '动态'
        verbose_name_plural = verbose_name
        ordering = ['-created_at']

    def __str__(self):
        return self.content

    def get_parent(self):
        """查找是否有父推文"""
        if self.parent:
            return self.parent
        else:
            return self

    def get_all_comment(self):
        """获取推文的所有评论"""
        parent = self.get_parent()
        return parent.thread.all()

    def comment_count(self):
        """获取推文的评论总数"""
        return self.get_all_comment().count()

    # def get_all_liked_user(self):
    #     return self.liked_user.all()
    #
    # def like_user_count(self):
    #     return self.liked_user.count()

    def switch_like(self, user):
        # 如果用户已经点赞过，则取消赞
        if user in self.liked_user.all():
            self.liked_user.remove(user)
        # 如果用户没有赞过，则添加赞
        else:
            self.liked_user.add(user)

    def tweet_comment(self, user, text):
        """
        评论推文
        :param user: 登录的用户
        :param text: 回复的内容
        :return: None
        """
        parent = self.get_parent()
        Tweet.objects.create(user=user, content=text,
                             reply=True, parent=parent,)