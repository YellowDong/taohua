from django.db import models
from django.utils.timezone import now
from uuslug import slugify
from abc import abstractmethod, abstractproperty, ABCMeta
from django.contrib.sites.models import Site
from mdeditor.fields import MDTextField
from django.conf import settings


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
    body = MDTextField('正文')
    pub_time = models.DateTimeField('发布时间', blank=True, null=True)
    status = models.CharField('文章状态', max_length=1, choices=STATUS_CHOICES, default='p')
    comment_status = models.CharField('评论状态', max_length=1, choices=COMMENT_STATUS, default='o')
    type = models.CharField('类型', max_length=1, choices=TYPE, default='a')
    views = models.PositiveIntegerField('浏览量', default=0)
    author = models.ForeignKey(settings.AUTH_USER_MODEL, verbose_name='作者', on_delete=models.CASCADE)
    article_order = models.IntegerField('排序,数字越大越靠前', blank=False, default=0, null=False)
    tags = models.ManyToManyField('Tag', verbose_name='标签集合', blank=True)
    category = models.ForeignKey('Category', verbose_name='分类', on_delete=models.CASCADE)

    class Meta:
        ordering = ['-pub_time']
        verbose_name_plural = verbose_name = '文章'


class Tag(BaseModel):
    """文章标签"""
    name = models.CharField('标签名', max_length=30, unique=True)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    def __str__(self):
        return self.name

    def get_article_count(self):
        return Article.objects.filter(tags__name=self.name)

    class Meta:
        ordering = ['name']
        verbose_name_plural = verbose_name = '标签'


class Category(BaseModel):
    name = models.CharField('分类名', max_length=30, unique=True)
    parent_category = models.ForeignKey('self', verbose_name='父级分类', blank=True, null=True, on_delete=models.CASCADE)
    slug = models.SlugField(default='no-slug', max_length=60, blank=True)

    class Meta:
        ordering = ['name']
        verbose_name_plural = verbose_name = '分类'

    def __str__(self):
        return self.name

    def get_category_tree(self):
        """递归获得分类目录的
        :return:
        """
        categorys = []

        def parse(category):
            categorys.append(category)
            if category.parent_category:
                parse(category.parent_category)

        parse(self)
        return categorys



