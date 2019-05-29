from django.db import models
from django.utils.timezone import now
from uuslug import slugify
from abc import abstractmethod, abstractproperty, ABCMeta
from django.contrib.sites.models import Site

from


class BaseModel(models.Model):
    created_time = models.DateTimeField('创建时间', default=now)
    last_mod_time = models.DateTimeField('修改时间', default=now)

    def save(self, force_insert=False, force_update=False, using=None,
             update_fields=None):
        if not isinstance(self, Article) and 'slug' in self.__dict__:
            if getattr(self, 'slug') == 'no-slug' or not self.id:
                slug = getattr(self, 'title') if 'title' in self.__dict__ else getattr(self, 'name')
                setattr(self, 'slug', slugify(slug))
        is_update_views = isinstance(self, Article) and update_fields == ['views']
        if is_update_views:
            Article.objects.filter(pk=self.pk).update(views=self.views)
        else:
            super().save()

    def get_current_url(self):
        site = Site.objects.get_current()
        return site

    def get_full_url(self):
        site = self.get_current_url().domain
        path = self.get_absolute_url()
        url = f'https://{site}{path}'
        return url

    class Meta:
        """abstract = True表示这个模型是一个抽象模型，在迁移数据库时抽象模型不会产生具体的数据表
        而是作为其它模型的父类，被继承使用"""
        abstract = True

    @abstractmethod
    def get_absolute_url(self):
        """使用抽象方法装饰器装饰成一个抽象方法，没有实现，所以基类不能被实例化，子类必须实现该方法才能被实例化"""
        pass


class Article(BaseModel):
    """文章"""
    STATUS_CHOICES = (  # 可选择的参数，是一个元组，第一个参数存数据库，第二个参数用来显示
        ('d', '草稿'),
        ('p', '发表'),
    )
    COMMENT_STATUS = (
        ('o', '打开'),
        ('c', '关闭'),
    )
    TYPE = (
        ('a', '文章'),
        ('p', '页面'),
    )
    title = models.CharField('标题', max_length=200, unique=True)
    body = models.
