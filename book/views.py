from django.contrib import auth

import xadmin
from django.core.cache import cache
from django.http import JsonResponse

from django.shortcuts import render
import reversion

from user.models import User
from .models import *


# Create your views here.

def book_info(request, pk):
    book = Book.objects.filter(pk=pk, is_show=True).first()
    print(book.authors)
    categorys = BookCategory.objects.all()
    is_in_rock = None
    # if request.user.is_authenticated:
    #     is_in_rock = request.user.book_rack.book.filter(id=pk)
    return render(request, 'book_info.html', locals())
import time
from django.db.models import F
# models.UserInfo.objects.update(age = F('age') + 1)
def vote(request,book_pk):
    if not request.user.is_authenticated:
        data = {'status': 300, 'msg': '请先登录'}
        return JsonResponse(data)
    print('book_pk', book_pk)
    c_time = str(time.strftime('%Y%m%d'))
    key = str(request.user) + c_time
    if not cache.get(key):
        print('book_pk111',book_pk)

        Book.objects.filter(pk=book_pk).update(ballot = F('ballot') + 1)
        code=Book.objects.filter(pk=book_pk).first().ballot
        data = {'status':100,'code': code,'msg':'投票成功'}
        cache.set(key,1,5)
    else:
        print('今日点赞数达到上限')
        data = {'status': 200, 'msg': '今日点赞数达到上限'}
        print('今日点赞数达到上333限')


    return JsonResponse(data)

def ranking(request):
    user_obj = User.objects.filter(pk=request.user.pk).first()
    print(request.user.book_rack,type(request.user),user_obj.book_rack,request.user)
    book_query = Book.objects.all().order_by('-ballot')
    category_name = '小说排行'
    return render(request, 'book_category.html', locals())

#收藏小说
def book_rack(request,book_pk):
    data={'status':100,'msg':''}
    book_obj=Book.objects.filter(pk=book_pk).first()
    book_rack_obj=request.user.book_rack
    if not book_rack_obj:
        book_rack_obj=BookRack.objects.create()
        request.user.book_rack=book_rack_obj
        request.user.save()
    print('book_obj.book_rack',book_obj.book_rack)
    # book_obj.book_rack.add(book_rack_obj)
    # book_obj.book_rack.add(book_rack_obj)
    # data = {'status': 100, 'msg': '收藏成功'}
    book_obj_list=list(book_rack_obj.book.all())

    print('book_obj_list;   ',book_obj_list)
    if book_obj in book_obj_list:
        data = {'status': 200, 'msg': '该书已在书架中'}
    else:
        book_obj.book_rack.add(book_rack_obj)
        data = {'status': 100, 'msg': '收藏成功'}
    return JsonResponse(data)
    # user_obj=User.objects.filter(pk=request.user.pk).first()

def category(request, pk):
    print('time; ',time.strftime('%Y%m%d'))
    book_query = Book.objects.all()
    category_name='全部小说'
    if pk:
        category_obj = BookCategory.objects.filter(pk=pk).first()
        book_query = Book.objects.filter(book_category_id=pk).all()
        category_name = category_obj.category_name

    return render(request, 'book_category.html', locals())


def search(request,book_name):
    if book_name:
        name =book_name
        book_query = Book.objects.filter(book_title=name).all()
    if request.method == 'POST':
        choice = request.POST.get('choice')
        name = request.POST.get('name')
        if choice == '小说':
            book_query = Book.objects.filter(book_title=name).all()
            book_query2 = Book.objects.filter(book_title__contains=name).all()
            book_query = list(book_query) + list(book_query2)


        else:
            author_obj = Author.objects.filter(author_name=name)
            # author_id=author_obj.pk
            book_query = Book.objects.filter(author__in=author_obj).all()
    return render(request, 'book_category.html', locals())



def section(request, book_pk, num=None,num2=None):
    book_obj = Book.objects.filter(pk=book_pk).first()
    section_obj_query = BookContent.objects.filter(book=book_obj).all()
    section_obj_lis = list(section_obj_query)
    if not num:
        section_obj = section_obj_query.first()
    else:
        print('num,num2; ',num2,type(num2))
        if num2=='0':
            print('num2=0')
            num=int(num)-1
            if not BookContent.objects.filter(book_id=book_pk,pk=num):
                print('change')
                num+=1
        if num2=='1':
            num=int(num)+1

            if not BookContent.objects.filter(book_id=book_pk,pk=num):
                print('change1')
                num-=1

        index = int(num) - int(section_obj_query.first().pk)

        section_obj = section_obj_lis[index]

    return render(request, 'section.html', locals())

def video(request):
    video_lis=[{'aid':55545556,'cid':97115444,'book_name':'欧罗巴之敌'},
               {'aid':60381374,'cid':105121427,'book_name':'地球不需要系统'},
               {'aid':61787724,'cid':107444740,'book_name':'王者天下'},
               {'aid': 23459945, 'cid': 39139016, 'book_name': '我的极品女老师'},
               {'aid': 23459945, 'cid': 39139016, 'book_name': '我的极品女老师'},
               {'aid': 23459945, 'cid': 39139016, 'book_name': '我的极品女老师'},
               ]

    return render(request, 'book_video.html', locals())

def catalog(request,book_pk):
    book_obj = Book.objects.filter(pk=book_pk).first()
    section_obj_query = BookContent.objects.filter(book=book_obj).all()


def comment(request):
    back_dic = {'code':None,'msg':''}
    if request.is_ajax():
        comment = request.POST.get('comment')
        article_id = request.POST.get('article_id')
        parent_id = request.POST.get('parent_id')
        print(parent_id)
        with transaction.atomic():
            # 在with代码块写的就是一个事务
            # 文章表修改comment_num字段
            models.Article.objects.filter(pk=article_id).update(comment_num = F('comment_num') + 1)
            # 评论表里面新增数据
            models.Comment.objects.create(user=request.user,article_id=article_id,content=comment,parent_id=parent_id)
        back_dic['code'] = 2000
        back_dic['msg'] = '评论成功'
    return JsonResponse(back_dic)


