from django.test import TestCase
import os,django,requests
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "connorshare.settings")# project_name 项目名称
django.setup()
import urllib.request
import re,json
from book.models import *
from requests_html import HTMLSession,HTML



import redis
pool = redis.ConnectionPool(host='127.0.0.1', port=6379)
#host='127.0.0.1', port=6379  为默认值,可不传,可传最大连接数
r = redis.Redis(connection_pool=pool)


def getNovelContent():
    session = HTMLSession()
    # url = "https://www.qiushibaike.com/text/"


    html = urllib.request.urlopen("https://www.183xsw.com/paihangbang/newbook.html").read()
    html = html.decode("gbk")
    book_html = '<li>(\d)<a href="(.*?)">(.*?)</a></li>'
    urls = re.findall(book_html, html)
    # print('urls: ',urls)
    # 遍历排行榜小说
    for i in urls:
        novel_url = i[1]
        novel_name = i[2]
        print('书名; ',novel_name)
        if r.get(novel_url):
            continue
        # h = session.get(url=novel_url)
        # print(123,h.html.html)

        # print(h.html.links)
        # for _ in h.html.links:
        #     print(_)
        novel_site = urllib.request.urlopen(novel_url).read()
        # print('进入小说主页')
        novel_html = novel_site.decode("gbk")
        # print(novel_html)
        # 获取小说封面,作者,简介等信息
        book_image_reg='<meta property="og:image" content="(.*?)"/>'
        book_category_reg='<a href="/">183小说网</a> &gt; <a href="/(.*?)/">(.*?)</a>  &gt;'
        # 0.名字,1.作者
        book_detail_reg= '<p>作&nbsp;&nbsp;&nbsp;&nbsp;者：(.*?)</p>'

        book_image=re.findall(book_image_reg, novel_html)[0]
        book_category=re.findall(book_category_reg, novel_html)[0][1]
        print(book_category)
        book_detail=re.findall(book_detail_reg, novel_html)
        print('作者; ',book_detail)
        print()
        author=book_detail[0]
        #获取章节
        section_reg='<dd><a href="(.*?)">(.*?)</a></dd>'
        section_htmls=re.findall(section_reg, novel_html)
        # print('section_htmls; ',section_htmls)
        j=0
        for section_html in section_htmls:
            j+=1
            if j>10:
                r.set(novel_url,1)
                break
            section_url1=section_html[0]
            if r.get(section_url1):
                continue

            section_url='https://www.183xsw.com'+section_url1  #章节地址
            # print('section_url; ',section_url)
            section_name=section_html[1]  #章节名
            section_content=urllib.request.urlopen(section_url).read()

            section_html = section_content.decode("gbk",errors='ignore')

            # content_reg='&nbsp;&nbsp;&nbsp;&nbsp;(.*?)<br />'
            content_reg='&nbsp;&nbsp;&nbsp;&nbsp;.*?<br />'
            content=re.findall(content_reg,section_html)
            # print('content; ',content)
            # content=content[0].replace("&nbsp;&nbsp;&nbsp;&nbsp;", "")
            # content=content.replace('<br />','')
            print("正在下载：{}".format(section_name))
            #将章节写入文件
            path=r'/media/section_content'+'/{}'.format(novel_name)
            path='.'+path
            if not os.path.exists(path):

                print(path)
                os.mkdir(path)

            s_path='section_content/{}/{}.txt'.format(novel_name,section_name)
            path = path+'/{}.txt'.format(section_name)

            f = open(path, "w")
            for c in content:
                f.write(c)
                # f.write('&nbsp;&nbsp;&nbsp;&nbsp;{}<br />'.format(c))
            f.close()
            #将图片存入本地
            pic = requests.get(book_image, timeout=10)
            cover = 'book_cover/' + novel_name + '.jpg'
            dir='media/'+cover
            fp = open(dir, 'wb')
            fp.write(pic.content)
            fp.close()

            #添加数据
            import pymysql
            db = pymysql.connect(host='localhost', user='root', password='360121')
            db.select_db('my_novel')
            db.set_charset('utf8')
            cursor = db.cursor()

            # 开启事务
            db.begin()
            try:
                if not r.get('book_name').decode() == novel_name:

                    r.set('book_name', novel_name)
                    BookCategory_obj = BookCategory.objects.filter(category_name=book_category).first()
                    if not BookCategory_obj:
                        BookCategory_obj = BookCategory.objects.create(category_name=book_category)
                    book_obj = Book.objects.create(book_title=novel_name, book_cover=cover, book_category=BookCategory_obj)
                    author_obj = Author.objects.create(author_name=author)
                    book_obj.author.add(author_obj)

                    db.commit()
            except Exception as e:
                    print(e)
                    # 回滚所有操作
                    db.rollback()
            cursor.close()
            db.close()
            book_obj=Book.objects.filter(book_title=novel_name).first()
            print(book_obj)
            BookContent.objects.create(section=section_name,section_content=s_path,book=book_obj)


            #将章节链接存入redis,避免重复下载
            r.set(section_url1, 1)
        r.set(novel_url, 1)
if __name__=='__main__':
    getNovelContent()
