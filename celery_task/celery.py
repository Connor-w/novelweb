from celery import Celery
broker = 'redis://127.0.0.1:6379/1'

backend = 'redis://127.0.0.1:6379/2'
app = Celery('celery_demo', broker=broker, backend=backend, include=['celery_task.tasks'])
# 时区
app.conf.timezone = 'Asia/Shanghai'
# 是否使用UTC
app.conf.enable_utc = False

# 配置任务
from datetime import timedelta
from celery.schedules import crontab
app.conf.beat_schedule = {
    'add-every-3-seconds': {
        'task': 'celery_task.tasks.getNovelContent',
        'schedule': timedelta(seconds=100),
        'args': (),
    },
    # 'low-every-6-seconds': {
    #     'task': 'celery_task.tasks.low',
    #     'schedule': timedelta(seconds=6),
    #     'args': (3000, 1000),
    # },
    # 'add-every-time': {
    #     'task': 'celery_task.tasks.add',
    #     # 设置定时
    #     'schedule': crontab(month_of_year=1, day_of_month=1, hour=0, minute=0),
    #     'args': (3000, 1000),
    # }
}




