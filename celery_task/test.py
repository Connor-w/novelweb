import os,django,requests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "connorshare.settings")# project_name 项目名称
django.setup()
from book.models import *
obj=Book.objects.all()
print(obj)