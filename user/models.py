

# Create your models here.
from django.db import models
from django.contrib.auth.models import AbstractUser
from book.models import *


class User(AbstractUser):
    phone_number = models.CharField(max_length=15, unique=True, null=True, verbose_name='手机号')
    avatar = models.ImageField(upload_to='avatar/', default='avatar/default_avatar.jpg', blank=True,
                               verbose_name='用户头像',
                               help_text='头像图片的大小规格：256x256，或者对应的比例的图片')
    register_time = models.DateTimeField(auto_now_add=True, null=True, blank=True, verbose_name="注册时间")
    is_vip = models.BooleanField(default=False, verbose_name="会员")
    vip_expire_time = models.DateTimeField(null=True, verbose_name="会员过期时间", blank=True)
    is_alive = models.BooleanField(default=False, verbose_name="会员激活")
    is_delete = models.BooleanField(default=False, verbose_name="逻辑删除")
    #  ==<外键关联>:[一对一]==
    user_detail = models.OneToOneField(to="UserDetail", on_delete=models.CASCADE, null=True)
    user_site = models.OneToOneField(to="UserSite", on_delete=models.DO_NOTHING, null=True)
    book_rack = models.OneToOneField(to=BookRack, null=True, verbose_name="书架", on_delete=models.CASCADE)


    #  ==<外键关联>:[一对多]==

    #  ==<外键关联>:[多对多]==


    class Meta:
        db_table = "BoyReading_User"
        verbose_name_plural = "用户"

    def __str__(self):
        return self.username

    @property
    def detail(self):
        data = {
            'gender': self.user_detail.gender,
            'age': self.user_detail.age,
            'hobby': self.user_detail.hobby,
            'brief': self.user_detail.brief
        }
        return data

    @property
    def site_info(self):
        data = {'site_name': self.user_site.site_name,
                'site_title': self.user_site.site_title
                }
        return data



class UserDetail(models.Model):
    gender_choices = ((0, "男"), (1, "女"), (2, "未知"))
    gender = models.SmallIntegerField(choices=gender_choices, default=2, verbose_name="性别")
    age = models.IntegerField(null=True, verbose_name='年龄')
    hobby = models.CharField(max_length=255, null=True, verbose_name='爱好')
    brief = models.TextField(max_length=1024, null=True, verbose_name="个人概要", default='这个人很懒，什么都没留下!')

    class Meta:
        db_table = "BoyReading_UserDetail"
        verbose_name_plural = "用户详情"

    def __str__(self):
        return "[%s]详情" % self.user



class UserSite(models.Model):
    site_name = models.CharField(max_length=32, null=True)
    site_title = models.CharField(max_length=64, null=True)
    site_theme = models.CharField(max_length=64, null=True)

    class Meta:
        db_table = "BoyReading_UserSite"
        verbose_name_plural = "用户个人页"

    def __str__(self):
        return "用户[%s]个人页:%s" % (self.user, self.site_name)

class BaseModel(models.Model):
    create_time = models.DateTimeField(verbose_name='创建时间', auto_now_add=True)
    is_delete = models.BooleanField(verbose_name='是否删除', default=False)
    class Meta:
        # 有该属性的Model类不会完成数据库迁移产生一张表 - 基表
        abstract = True

class Comment(BaseModel):

    user = models.ForeignKey(to='User',related_name='comment',db_constraint=False,on_delete=models.CASCADE,verbose_name='用户名')
    section = models.ForeignKey(to=BookContent,related_name='comments',db_constraint=False,on_delete=models.CASCADE,verbose_name='用户名')
    content = models.TextField()

    parent = models.ForeignKey(to='self',null=True,blank=True,related_name='comment',db_constraint=False,on_delete=models.CASCADE,verbose_name='父级')
