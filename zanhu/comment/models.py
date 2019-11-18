from django.conf import settings
from django.db import models
from django.utils.translation import gettext_lazy as _
from django.contrib.contenttypes.fields import GenericForeignKey
from django.contrib.contenttypes.models import ContentType

COMMENT_MAX_LENGTH = getattr(settings, 'COMMENT_MAX_LENGTH', 3000)


# Create your models here.
class Comment(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE, verbose_name='用户')
    content = models.TextField(_('评论内容'), max_length=COMMENT_MAX_LENGTH)
    submit_date = models.DateTimeField(verbose_name='提交时间', auto_now_add=True)
    is_removed = models.BooleanField(verbose_name='是否删除', default=False,
                                     help_text=_('检查评论是否被删除，否则 "此评论已经被删除" 消息会发送'))

    # Generic Relations
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        ordering = ('-submit_date',)

    def __str__(self):
        return "%s..." % (self.content[:50])

