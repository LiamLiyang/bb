from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone
from django.contrib.auth.models import AbstractUser


class NewUser(AbstractUser):
    profile = models.CharField('profile', default='', max_length=256)

    def __str__(self):
        """
        admin 頁面顯示的的字段
        :return:
        """
        return self.username


class Column(models.Model):
    name = models.CharField('column_name', max_length=256)
    intro = models.TextField('introduction', default='')

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = 'column'
        verbose_name_plural = 'column'
        #orderin = ['name']


class Article(models.Model):
    """
    auto_now  每次 save時保存
    auto_now_add 第一save時保存
    editable   允許修改
    BooleanField 應該是bool
    """
    column = models.ForeignKey(Column, blank=True, null=True, verbose_name='belong to', db_column='分類')
    title = models.CharField(max_length=256, db_column='標題')
    author = models.ForeignKey('Author')
    user = models.ManyToManyField('NewUser', blank=True)
    content = models.TextField('content', db_column='文章')
    update_time = models.DateTimeField(auto_now=True, null=True, db_column='更新')
    pub_date = models.DateTimeField(auto_now_add=True, editable=True, db_column='創建')
    published = models.BooleanField('notDraft', default=True, db_column='是否發佈')
    poll_num = models.IntegerField(default=0)
    comment_num = models.IntegerField(default=0)
    keep_num = models.IntegerField(default=0)

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = 'article'
        verbose_name_plural = 'article'
        #ordering = ['-pub_date']


class Comment(models.Model):
    user = models.ForeignKey('NewUser', null=True)
    article = models.ForeignKey(Article, null=True)
    content = models.TextField()
    pub_date = models.DateTimeField(auto_now_add=True)
    pub_num = models.IntegerField(default=0)

    def __str__(self):
        return self.content


class Author(models.Model):
    name = models.CharField(max_length=256)
    profile = models.CharField('profile', default='', max_length=256)
    password = models.CharField('password', max_length=256)
    register_date = models.DateTimeField(auto_now_add=True, editable=True)

    def __str__(self):
        return self.name


class Poll(models.Model):
    user = models.ForeignKey('NewUser', null=True)
    article = models.ForeignKey(Article, null=True)
    comment = models.ForeignKey(Comment, null=True)
