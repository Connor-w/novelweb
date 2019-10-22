from django.forms import ModelForm
from django.shortcuts import render
from django.core.cache import cache
from rest_framework.views import APIView
from django.shortcuts import render,HttpResponse,redirect

from django.http import JsonResponse
from django.contrib import auth
from .common import *
from django.db.models.functions import TruncMonth
from django.db.models import F
from django.utils.safestring import mark_safe
from . import models
from book.models import *


# Create your views here.



class RegisterAPIView(APIView):
    def get(self, request, *args, **kwargs):
        form_obj=RegForm()
        return render(request,'register.html',locals())

    def post(self, request, *args, **kwargs):
        back_dic={'code':None,'msg':''}
        form_obj=RegForm(request.POST)
        if form_obj.is_valid():
            clean_data=form_obj.cleaned_data
            clean_data.pop('confirm_password')
            avatar=request.FILES.get('my_avatar')

            if avatar:
                clean_data['avatar']=avatar
            #auth模块创建普通用户方法,可以把密码处理成密文
            models.User.objects.create_user(**clean_data)
            back_dic['code']=2000
            back_dic['msg']='注册成功'
            back_dic['url']='/user/login.html'
        else:
            back_dic['code']=2001,
            back_dic['msg']=form_obj.errors
        return JsonResponse(back_dic)



class LoginAPIView(APIView):
    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self,request, *args, **kwargs):
        back_dic = {'code': None, 'msg': ''}
        username=request.POST.get('username')
        password=request.POST.get('password')
        code=request.POST.get('code')
        s_code=cache.get('code')
        if code:
            if s_code:
                if s_code.upper()==code.upper():
                    user_obj=auth.authenticate(username=username,password=password)
                    if user_obj:
                        auth.login(request,user_obj)
                        back_dic['code']=100
                        back_dic['msg']='登陆成功'
                        back_dic['username']=username,
                        back_dic['url']='/home/index.html'

                    else:
                        back_dic['code'] = 201
                        back_dic['msg'] = '用户名或密码错误'
                else:
                    back_dic['code'] = 202
                    back_dic['msg'] = '验证码错误'
            else:
                back_dic['code'] = 203
                back_dic['msg'] = '验证码失效'
        else:
            back_dic['code'] = 204
            back_dic['msg'] = '未填写验证码'
        return JsonResponse(back_dic)

class SiteAPIView(APIView):
    def get(self,request, *args, **kwargs):
        book_list = list(request.user.book_rack.book.all())
        return render(request, 'site.html',locals())





def loginout(request):
    auth.logout(request)
    return redirect(to='/home/index.html')


