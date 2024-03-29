from django.db import models

# Create your models here.
from django.db import models
class Banner(models.Model):
    """轮播图"""
    # upload_to 存储子目录，真实存放地址会使用配置中的MADIE_ROOT+upload_to
    image = models.ImageField(upload_to='banner', verbose_name='轮播图', null=True, blank=True)
    name = models.CharField(max_length=150, verbose_name='轮播图名称')
    note = models.CharField(max_length=150, verbose_name='备注信息')
    link = models.CharField(max_length=150, verbose_name='轮播图广告地址')
    orders = models.IntegerField(verbose_name='显示顺序')
    is_show=models.BooleanField(verbose_name="是否上架", default=False)
    is_delete=models.BooleanField(verbose_name="逻辑删除", default=False)

    class Meta:
        db_table = 'cx_banner'
        verbose_name = '轮播图'
        verbose_name_plural = verbose_name

    def __str__(self):
        return self.name