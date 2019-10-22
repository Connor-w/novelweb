import xadmin
from xadmin import views
from . import models


# 注册
# xadmin.site.register(models.User)
xadmin.site.register(models.UserDetail)
xadmin.site.register(models.UserSite)
