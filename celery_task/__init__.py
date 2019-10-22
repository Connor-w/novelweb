# app
from .celery import app
# tasks
from .tasks import *


# 在该包所在文件夹下执行
# 起执行任务的服务
# celery worker -A celery_task -l info -P eventlet

# 起提交任务的服务
# celery beat -A celery_task -l info

