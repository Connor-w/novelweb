from django.test import TestCase

# Create your tests here.
import urllib.request
import re


def getNovelContent():
    html = urllib.request.urlopen("http://www.quanshuwang.com/book/9/9055").read()
    html = html.decode("gbk")
    req = '<li><a href="(.*?)" title="(.*?)">(.*?)</a></li>'
    urls = re.findall(req, html)
    # 遍历每章（章节网址和名字）
    for i in urls:
        novel_url = i[0]
        novel_name = i[1]
        chapt = urllib.request.urlopen(novel_url).read()
        chapt_html = chapt.decode("gbk")
    # 获取小说内容
        print(chapt)
        reg = '</script>(.*?)<script type="text/javascript">'

        # 多行匹配
        reg = re.compile(reg, re.S)
        chapt_content = re.findall(reg, chapt_html)
        print(chapt_content)

        # 删掉多余的字符串（替换）
        chapt_content = chapt_content[0].replace("&nbsp:&nbsp:&nbsp:&nbsp", "")
        chapt_content = chapt_content.replace("<br />", "")
        # 下载小说
        print("正在下载：%s" % novel_name)
        f = open('{}.txt'.format(novel_name), "w")
        f.write(chapt_content)
        f.close()
        # 调用函数
getNovelContent()


