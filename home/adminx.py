import xadmin
from xadmin import views
from . import models

class GlobalSettings(object):
    """xadmin的全局配置"""
    site_title = "c享小说网"  # 设置站点标题
    site_footer = "www.connorshare.top"  # 设置站点的页脚
    menu_style = "accordion"  # 设置菜单折叠

xadmin.site.register(views.CommAdminView, GlobalSettings)

# 注册
xadmin.site.register(models.Banner)