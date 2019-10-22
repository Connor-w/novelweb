'''
爬取183小说网
'''

import re
import requests
import os
ssl._create_default_https_content=ssl._create_unverified_context

url='https://fanyi.baidu.com/sug'

# 得到Html内容
def getHtml(url):
    response = requests.get(url)
    response.encoding = "gbk"
    html = response.text
    return html;


'''
得到分类的图书url列表
'''


def get_sort_list(url):
    bookRe = r'<a target="_blank" title="(.*?)" href="(.*?)" class="clearfix stitle">'
    return re.findall(bookRe, getHtml(url))


'''
获得书的开始阅读目录url
'''


def get_novel_list(url):
    novelRe = r'<a href="(.*?)" class="reader" title=".*?">'
    return re.findall(novelRe, getHtml(url))[0];


'''
获得书章节url列表
'''


def get_chapter(url):
    chapterRe = r'<li><a href="(.*?)" title=".*?">(.*?)</a></li>'
    return re.findall(chapterRe, getHtml(url));


'''
获得书章节内容
'''


def get_chapter_content(url):
    chapterConRe = r'<script type="text/javascript">style5\(\);</script>(.*?)<script type="text/javascript">style6'
    chapterLi = re.findall(chapterConRe, getHtml(url), re.S)
    print(chapterLi)
    return chapterLi[0];


"主函数"
if __name__ == '__main__':
    url = "http://www.quanshuwang.com/list/8_1.html"
    # 得到分类的图书url列表
    bookLi = get_sort_list(url)

    for novel_name, novel_url in bookLi:
        print("novel_name:{} || novel_url:{}".format(novel_name, novel_url))
        path = os.path.join("novel", novel_name)
        if (not os.path.exists(path)):  # 创建文件夹
            os.mkdir(path)
            print("文件夹创建成功")
        else:
            print("文件夹已存在")

        # 获得书的开始阅读目录url
        novel_url = get_novel_list(novel_url)
        # print(novel_url)

        # 获得书章节url列表
        chapterLi = get_chapter(novel_url)
        # print(chapterLi)
        for chapter_url, chapter_name in chapterLi:
            # 获得书章节内容
            chapter_content = get_chapter_content(chapter_url)

            # 文件名里含\和/（半角），变成路径之后会被识别成目录，如果用＼和／（全角）替换
            # 转换方法：
            # string = string.replace('/', chr(ord('/') + 65248)).replace('\\', chr(ord('\\') + 65248))
            ##除空格外半角+65248=全角 另外注意\的转意 所以用\\
            # path = r'第107章 传送阵【1/10，求订阅】'.replace('/',chr(ord('/')+65248))

            with open(os.path.join(path, chapter_name.replace('/', chr(ord('/') + 65248)) + ".html"), "w") as f:
                print(os.path.join(path, chapter_name.replace('/', chr(ord('/') + 65248)) + ".html"))
                f.write(chapter_content)
        break

    # get_chapter_content(novelList)

    # print(bookLi)
