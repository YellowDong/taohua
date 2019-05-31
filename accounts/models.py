from django.db import models
from django.contrib.auth.models import AbstractUser, BaseUserManager
# from django.urls import reverse
from django.utils.timezone import now
# from django.contrib.sites.models import Site


class TaoHuaUser(AbstractUser):
    nickname = models.CharField('昵称', max_length=100, blank=True)
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)

    class Meta:
        ordering = ['-id']
        verbose_name_plural = verbose_name = '用户'
        get_latest_by = 'id'

    def __str__(self):
        return self.email

    # def get_absolute_url(self):
    #     return reverse('blog:author_detail', kwargs={'author_name': self.username})
    #
    # def get_current_url(self):
    #     site = Site.objects.get_current()
    #     return site
    #
    # def get_full_url(self):
    #     site = self.get_current_url().domain
    #     path = self.get_absolute_url()
    #     url = f'https://{site}{path}'
    #     return url
