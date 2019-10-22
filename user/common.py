from django.shortcuts import render,HttpResponse
from django.core.cache import cache
from PIL import Image,ImageDraw,ImageFont
from . import models
from io import BytesIO
import random
def get_random():
    return random.randint(0,255),random.randint(0,255),random.randint(0,255)

def get_code(request):
    """
    1.文件存储麻烦
    2.文件颜色随机变化
    """
    # 最终不删减版
    img_obj = Image.new('RGB',(260,35),get_random())
    img_draw = ImageDraw.Draw(img_obj)  # 在当前图片上生成一个画笔
    img_font = ImageFont.truetype('media/static/font/222.ttf',30)

    # 图片验证码 (数字 小写字母 大写字母)  五位验证码  1aZd2
    # A-Z:65-90  a-z:97-122
    # 定义一个变量用来存储验证码
    code = ''
    for i in range(5):
        upper_str = chr(random.randint(65,90))
        lower_str = chr(random.randint(97,122))
        random_int = str(random.randint(0,9))
        # 从上面三个里面随机选择一个
        res = random.choice([upper_str,lower_str,random_int])
        img_draw.text((40 + i * 40, -5), res, get_random(), img_font)
        code += res
    print(code)
    # 保存

    io_obj = BytesIO()
    img_obj.save(io_obj,'png')
    # 找一个公共的地方 存储验证码 以便后续其他视图函数 校验
    # request.session['code'] = code
    cache.set('code',code,300)
    # 将写好字的图片返回出来
    return HttpResponse(io_obj.getvalue())


from django import forms
class RegForm(forms.Form):
    username = forms.CharField(max_length=8,min_length=3,label='用户名',
                               error_messages={
                                   'max_length':'用户名最长八位',
                                   'min_length':'用户名最短三位',
                                   'required':'用户名不能为空'
                               },widget=forms.widgets.TextInput(attrs={"class":'form-control'})
                               )
    password = forms.CharField(max_length=8, min_length=3, label='密码',
                               error_messages={
                                   'max_length': '密码最长八位',
                                   'min_length': '密码最短三位',
                                   'required': '密码不能为空'
                               }, widget=forms.widgets.PasswordInput(attrs={"class": 'form-control'})
                               )
    confirm_password = forms.CharField(max_length=8, min_length=3, label='确认密码',
                               error_messages={
                                   'max_length': '确认密码最长八位',
                                   'min_length': '确认密码最短三位',
                                   'required': '确认密码不能为空'
                               }, widget=forms.widgets.PasswordInput(attrs={"class": 'form-control'})
                               )
    email = forms.EmailField(label='邮箱',error_messages={
        'invalid':'邮箱格式错误',
        'required':'邮箱不能为空'
    },widget=forms.widgets.EmailInput(attrs={'class':'form-control'}))

    # 局部钩子  判断当前用户名是否存在
    def clean_username(self):
        username = self.cleaned_data.get('username')
        user_obj = models.User.objects.filter(username=username).first()
        if user_obj:
            self.add_error('username','用户名已存在')
        else:
            return username

    # 全局钩子  校验两次密码是否一直
    def clean(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if not password == confirm_password:
            self.add_error('confirm_password','两次密码不一致')
        else:
            return self.cleaned_data