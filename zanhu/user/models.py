# -*- coding:utf8 -*-
from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import gettext_lazy as _
from django.utils import timezone
from sorl.thumbnail import ImageField
# Create your models here.


class User(AbstractUser):
    """ 继承自AbstractUser """
    # 此类里面有很多字段和方法可以调用
    location = models.CharField(_('所在地'), max_length=50, null=True, blank=True)
    introduction = models.TextField(_('简介'), max_length=50, null=True, blank=True)
    picture = ImageField(_('头像'), upload_to='profile_pics/', null=True, blank=True)
    update_at = models.DateTimeField(_('更新时间'), auto_now=timezone.now, )
    gender_choices = (
        (u'M', u'男'),
        (u'F', u'女'),
    )
    gender = models.CharField(max_length=2, choices=gender_choices, null=True, blank=True)

    class Meta:
        verbose_name = _('user')
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.username
