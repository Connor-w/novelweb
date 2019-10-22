import xadmin
from xadmin import views
from . import models


# 注册
xadmin.site.register(models.Author)
xadmin.site.register(models.Book)
xadmin.site.register(models.BookCategory)
xadmin.site.register(models.BookRack)
xadmin.site.register(models.BookContent)
